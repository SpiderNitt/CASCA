#! /bin/bash
sudo su
apt-get update && apt-get install -y zip unzip python3 python3-pip python-pyx python-matplotlib tcpdump python-crypto graphviz imagemagick gnuplot python-gnuplot libpcap-dev && apt-get clean

apt-get update && apt-get install -y bridge-utils net-tools iptables python3 tcpdump build-essential python3-dev libnetfilter-queue-dev python3-pip libnfnetlink-dev libnetfilter-queue-dev

python3 -m venv .

source bin/activate

pip3 install -r requirements.txt 

echo "Created the virtual environment & Installed necessary packages"