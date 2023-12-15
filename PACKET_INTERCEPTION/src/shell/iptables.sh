# Route the packets to netfilterqueue
source .env
iptables -t raw -A PREROUTING -j NFQUEUE --queue-num $QUEUE_NUM
iptables -t raw -A OUTPUT -j NFQUEUE --queue-num $QUEUE_NUM
echo "Configured IP tables successfully"