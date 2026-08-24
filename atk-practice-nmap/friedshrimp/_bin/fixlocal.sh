#!/bin/bash
/etc/init.d/xinetd restart
cd /home/student/labtainer/trunk/labs/nmap-discovery/friedshrimp
date > result.txt
echo "This is a random result: $(date)" >> result.txt
