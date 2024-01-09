#!/usr/bin/env bash

set -euo pipefail

input=$1
output_dir=$2
output="${input%.*}.mp3"

ffmpeg -i "${input}" -af loudnorm=I=-16 -ar 44100 -c:a libmp3lame -q:a 2 "${output}"
