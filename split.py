#!/usr/bin/env python3

import os
import subprocess
import sys

input_file=sys.argv[1]
output_dir=sys.argv[2]
silence_duration=sys.argv[3] if len(sys.argv) > 3 else '2'
output_basename, output_extension = os.path.splitext(os.path.basename(input_file))

print('===> detecting silence in ' + input_file + ' with duration ' + silence_duration)

# Run silencedetect and store the output in a variable
silence_log = subprocess.run(['ffmpeg', '-i', input_file, '-af', f'silencedetect=d={silence_duration}', '-f', 'null', '-'], check=True, capture_output=True).stderr.decode('utf-8')

# Extract lines containing silence_start or silence_end
lines = [line for line in silence_log.split('\n') if 'silence_start' in line or 'silence_end' in line]

output_idx = 1

# fake a silence that ends when the track starts
lines.insert(0, "silence_end: 0 | silence_duration: 0.0")

# fake a silence that starts when the track ends
lines.append("silence_start: 999999")

# Write the non-silence parts to files
for i in range(0, len(lines), 2):
    end_time = lines[i].split(": ")[1].split(" |")[0].strip()
    start_time = lines[i + 1].split(": ")[1].strip()
    output_file = f"{output_basename}-{output_idx:03}{output_extension}"
    
    if end_time == start_time:
        print(f"===> Skipping {end_time} .. {start_time}")
        continue

    if os.path.exists(output_file):
        raise FileExistsError(f"Output file '{output_file}' already exists. Aborting.")

    ffmpeg_command = ['ffmpeg', '-i', input_file, '-ss', end_time, '-to', start_time, '-c', 'copy', output_file]
    print(f"===> Writing {output_file} ({end_time} .. {start_time})")
    try:
        subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        print(exc.stderr)
        raise

    output_idx += 1

