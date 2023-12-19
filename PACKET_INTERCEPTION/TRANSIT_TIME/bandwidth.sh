#!/bin/bash
args=("$@")
server_ip=${args[0]}
time_interval=${args[1]}
result=$(iperf -c "$server_ip" -t "$time_interval" -f m | grep -E "sec")
bandwidth=$(echo "$result" | awk '{print $7 $8}')

echo "$bandwidth"

