# Route the packets to netfilterqueue
source .env
if [[ $INCOMING_TRAFFIC == "true" ]]; then
    sudo iptables -t raw -A PREROUTING -p tcp --source-port 80 -j NFQUEUE --queue-num 1
else
    sudo iptables -t raw -A OUTPUT -p tcp --destination-port 80 -j NFQUEUE --queue-num 1
fi