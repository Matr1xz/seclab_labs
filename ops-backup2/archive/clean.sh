#!/bin/sh

sleep 5

while true; do
  find /home -type f -name "*.dump" -exec rm -f {} + 2>/dev/null
  find /home -type f -name "*.dump.*" -exec rm -f {} + 2>/dev/null
  sleep 5
done
