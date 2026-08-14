#!/bin/bash
log_file="/var/log/rkhunter.log"
recipient_email="your_email@gmail.com" 
date=$(date +"%Y-%m-%d %H:%M:%S") 
log_dir="/var/log/rkhunter"
mkdir -p $log_dir
current_log_file="$log_dir/rkhunter_scan_$(date +"%Y%m%d%H%M%S").log" 
echo $date
echo $current_log_file
echo "[$date] Running rkhunter scan..." >> “$current_log_file”
sudo rkhunter --check --skip-keypress >> “$current_log_file” 2 >&1

summary=$(grep -A 10 "System checks summary" "$current_log_file") 
warnings=$(grep "Warning" "$current_log_file")
echo "$summary"
echo "$warnings"
