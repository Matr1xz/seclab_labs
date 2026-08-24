#!/bin/bash
sudo snort -A console -q -c /etc/snort/snort.conf -i eth0 -k none 2>&1 | sudo tee -a /var/log/snort/snort.log
