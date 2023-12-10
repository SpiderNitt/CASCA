# Route the packets to netfilterqueue
source .env
iptables -t raw -A PREROUTING -p tcp --source-port 80 -j NFQUEUE --queue-num $QUEUE_NUM
iptables -t raw -A OUTPUT -p tcp --destination-port 80 -j NFQUEUE --queue-num $((QUEUE_NUM+1))
echo "Configured IP tables successfully"