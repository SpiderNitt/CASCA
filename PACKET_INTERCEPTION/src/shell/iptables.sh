# Route the packets to netfilterqueue
iptables -t raw -A PREROUTING -p tcp --source-port 80 -j NFQUEUE --queue-num 1
iptables -t raw -A OUTPUT -p tcp --destination-port 80 -j NFQUEUE --queue-num 2
echo "Configured IP tables successfully"