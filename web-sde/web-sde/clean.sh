#!/bin/sh

sleep 5

while true; do
    find /home -type d \( -name "webdriver" -o -name ".mozilla" -o -name ".cache" -o -name "sessions" \) \
        -exec rm -rf {} + 2>/dev/null

    sleep 1
done
