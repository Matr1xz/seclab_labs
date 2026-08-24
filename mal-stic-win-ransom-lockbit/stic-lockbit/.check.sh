#!/bin/bash

SOURCE="share2/log.txt"
DEST="log.txt"
SOURCE1="share2/result.txt"
DEST1="result.txt"

touch "$DEST"
touch "$DEST1"
if [ -f "$SOURCE" ]; then
    cp "$SOURCE" "$DEST"
fi
if [ -f "$SOURCE1" ]; then
    cp "$SOURCE1" "$DEST1"
fi
