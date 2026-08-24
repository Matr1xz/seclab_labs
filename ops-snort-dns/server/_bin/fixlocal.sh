#!/bin/bash
#
#  This script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument,
#  (the user ID is the second parameter)
#  If this script is to use sudo and the sudoers for the lab
#  does not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
#  If you issue commands herein to start services, and those services
#  have unit files prescribing their being started after the
#  waitparam.service, then first create the flag directory that
#  waitparam sleeps on:
#
#   PERMLOCKDIR=/var/labtainer/did_param
#   echo $1 | sudo -S mkdir -p "$PERMLOCKDIR"
sudo apt-get purge -y dnsmasq
sudo sed -i '/directory/a  dump-file "/var/cache/bind/dump.db";\nallow-query {any;};\nallow-query-cache {any;};\nallow-recursion {any;};\nlisten-on port 5353 {any;};' /etc/bind/named.conf.options
sudo sed -i 's/dnssec-validation auto;/dnssec-enable no;\ndnssec-validation no;/' /etc/bind/named.conf.options
# define example.com
echo "include \"/etc/bind/example.conf\";" | sudo tee -a /etc/bind/named.conf.local
sudo chown bind:bind /var/bind/*
echo "check alive" >> /tmp/fixlocal.output
~/.local/bin/alive.sh 10.10.19.5
echo "back and alive" >> /tmp/fixlocal.output
date >> /tmp/fixlocal.output
sleep 3
sudo /etc/init.d/bind9 restart
