#!/usr/bin/env bash

set -euxo pipefail

input=$1
output_dir=$2
input_filename=$(basename "${input}")
output="${output_dir}/${input_filename%.*}.mp3"

ffmpeg -i "${input}" -af loudnorm=I=-16 -ar 44100 -c:a libmp3lame -q:a 2 "${output}"
