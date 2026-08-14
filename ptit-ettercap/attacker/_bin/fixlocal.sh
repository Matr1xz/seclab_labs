sudo sysctl net.ipv4.conf.all.forwarding=0
sudo chmod 777 /home/ubuntu/logging
echo -n "Mail: " | cat - /home/ubuntu/.local/.email > /home/ubuntu/mail.txt
