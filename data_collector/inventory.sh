#!/bin/bash

api_url=http://inventoryapp.example.com:9001/api/computer

sudo /opt/scripts/inventory_app/venv/bin/python /opt/scripts/inventory_app/main.py
#echo ZALLOOOPA | /usr/bin/curl --silent --header "Content-Type: application/json" -d @- $api_url
