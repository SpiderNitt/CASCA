#!/bin/bash
#run as root

apt-get update && apt-get install -y python3 python3-pip

python3 -m venv .

source bin/activate

pip3 install -r requirements.txt 

echo "Created the virtual environment & Installed necessary packages"