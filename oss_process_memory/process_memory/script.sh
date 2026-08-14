#!/bin/bash

for i in {1..10000}
do
    echo "Lan $i - thoi gian: $(date)"
    while true; do head -c 100M /dev/urandom > /dev/null; done
    sleep 1
done
