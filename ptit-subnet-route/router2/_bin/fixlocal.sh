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
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forwarding
#sudo ip route add 172.16.1.0/24 via 172.16.2.1

