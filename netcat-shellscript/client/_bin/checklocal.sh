#!/bin/bash
#
#
echo -n "My string is: $(head -c 20 /dev/urandom | base64)" > sendfile.txt
