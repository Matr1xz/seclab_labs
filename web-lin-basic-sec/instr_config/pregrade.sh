#!/bin/bash
homedir=$1
destdir=$2
cd $homedir/$destdir

if [[ "$destdir" == *"client"* ]]; then
   find . -type f -name "*stdout*" | xargs grep -q "80" 2>/dev/null && echo "firewall_ok" >> client_result.txt
   find . -type f -name "*stdout*" | xargs grep -q "nosniff" 2>/dev/null && echo "header_ok" >> client_result.txt
fi
