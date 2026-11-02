#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <video_file> <number_of_frames>"
  exit 1
fi

VIDEO="$1"
NUM_FRAMES="$2"

ffmpeg -ss 00:00:01.000 -i "$VIDEO" -frames:v "$NUM_FRAMES" -vsync 0 "frame_%d.png" -loglevel error

if [ $? -eq 0 ]; then
  echo "Successfully extracted $NUM_FRAMES frames from $VIDEO"
else
  echo "Failed to extract frames from $VIDEO."
fi










