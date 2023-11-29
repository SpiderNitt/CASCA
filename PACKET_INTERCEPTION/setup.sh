#! /bin/bash
python3 -m venv .

source bin/activate

pip3 install -r requirements.txt 

echo "Created the virtual environment & Installed necessary packages"