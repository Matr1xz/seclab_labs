#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#  The container user password will be passed as the first argument.
#  Thus, if this script is to use sudo and the sudoers for the lab
#  not not permit nopassword, then use:
#  echo $1 | sudo -S the-command
#
sudo chmod 666 /dev/null
# Fix Student.py for Python 2.5 compatibility
if [ -f /home/ubuntu/.local/bin/Student.py ]; then
    sed -i 's/0o666/0666/g' /home/ubuntu/.local/bin/Student.py
fi
