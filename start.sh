#!/bin/bash

sudo apt install python3 python3-pip python3-setuptools
sudo pip3 install pymsql, flask, gnupg

echo "Starting Itrago Web Tool"
screen -AmdS web python3 app.py
echo "Starting Emergency Shell"
screen -AmdS shell python3 shell.py

screen -ls
