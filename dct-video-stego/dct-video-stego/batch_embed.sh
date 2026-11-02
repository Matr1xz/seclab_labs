#!/bin/bash

if [ ! -f embed.py ]; then
  echo "File embed.py not exist!"
  exit 1
fi

for txtfile in line_*.txt; do
  index=$(echo "$txtfile" | grep -oP '\d+')

  input_image="frame_${index}.png"
  output_image="frame_${index}_stego.png"

  if [ -f "$input_image" ]; then
    echo "Embedding $txtfile into $input_image -> $output_image"
    python3 embed.py "$txtfile" "$input_image" "$output_image"
  else
    echo "$input_image not found."
  fi
done

