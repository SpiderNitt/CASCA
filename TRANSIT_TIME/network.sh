#!/bin/bash
args=("$@")
server_ip=${args[0]}

result=$(iperf -c "$server_ip" -t 1 -f m | grep -E "sec")
bandwidth=$(echo "$result" | awk '{print $7 $8}')

# Measure latency
ping_result=$(ping -c 1 "$server_ip")
avg_latency=$(echo "$ping_result" | grep "rtt" | awk -F '/' '{print $5}')

echo "$bandwidth"
echo "$avg_latency"

