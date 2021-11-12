#!/bin/bash

pip install -r requirements.txt
chmod +rx app.py

echo
echo
echo "Running python script"
echo

./app.py -s btcusd -t all -p 10
