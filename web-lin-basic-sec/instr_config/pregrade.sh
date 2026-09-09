#!/bin/bash
homedir=$1
destdir=$2
cd $homedir/$destdir

if [[ "$destdir" == *"client"* ]]; then
   if grep -rq "80" .local/result/ 2>/dev/null; then
       echo "firewall_ok" >> client_result.txt
   fi

   if grep -rq "nosniff" .local/result/ 2>/dev/null; then
       echo "header_ok" >> client_result.txt
   fi
fi
