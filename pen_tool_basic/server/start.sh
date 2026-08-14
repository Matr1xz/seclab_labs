#!/bin/bash
# Script khởi động container

# Đợi 10 giây trước khi thực thi các lệnh
#echo "Waiting for 10 seconds..."
#sleep 30

# Thiết lập các iptables rules
iptables -A INPUT -p tcp --dport 21 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
#iptables -A INPUT -p tcp --dport 23 -j REJECT
#iptables -A INPUT -p tcp --dport 25 -j REJECT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
#iptables -A INPUT -p tcp --dport 111 -j REJECT
iptables -A INPUT -p tcp --dport 139 -j ACCEPT
iptables -A INPUT -p tcp --dport 445 -j ACCEPT
#iptables -A INPUT -p tcp --dport 512 -j REJECT
#iptables -A INPUT -p tcp --dport 513 -j REJECT
#iptables -A INPUT -p tcp --dport 514 -j REJECT
#iptables -A INPUT -p tcp --dport 1524 -j REJECT
#iptables -A INPUT -p tcp --dport 2121 -j REJECT
#iptables -A INPUT -p tcp --dport 3306 -j REJECT
#iptables -A INPUT -p tcp --dport 5432 -j REJECT
iptables -A INPUT -p tcp --dport 8009 -j ACCEPT
iptables -A INPUT -p tcp --dport 8180 -j ACCEPT

# Thực hiện các lệnh khởi động khác
echo "Container started and iptables rules applied."
echo "Container started and iptables rules applied."
echo "Container started and iptables rules applied."
echo "Container started and iptables rules applied."
echo "Container started and iptables rules applied."
# Đảm bảo container không kết thúc ngay lập tức
sudo /usr/sbin/vsftpd /etc/vsftpd.conf &
sudo /usr/sbin/sshd -D &
sudo /usr/sbin/apache2ctl start
sudo /usr/sbin/smbd -D
sudo JAVA_HOME=/usr/lib/jvm/java-gcj/jre /usr/share/tomcat5.5/bin/startup.sh
tail -f /dev/null

