#!/bin/bash

for file in frame_*_stego.png; do
    number=$(echo "$file" | grep -oP '(?<=frame_)\d+(?=_stego\.png)')
    
    formatted_number=$(printf "%04d" "$number")
    
    dest="frames/frame_${formatted_number}.png"
    
    cp "$file" "$dest"
    echo "Copied $file to $dest"
done
