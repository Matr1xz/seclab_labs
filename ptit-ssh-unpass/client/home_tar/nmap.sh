#!/bin/bash

# Define the IP address as a variable
ip_address="$1"

# Define the output file
output_file="/etc/nmap.out"

# Run the nmap command and save the output to the specified file
nmap "$ip_address" > "$output_file" 2>&1 &

# Wait for the nmap command to complete
wait

# Print the contents of the output file to stdout
cat "$output_file"

# Exit the script
exit 0
