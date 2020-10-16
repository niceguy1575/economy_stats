#!/bin/bash

echo "change the auth src"
chmod 777 /root/economy_stats/stock_index/src

echo "0. check and install pakcages."
python3 /root/economy_stats/stock_index/src/check_and_install_packages.py
echo "1. get stock data"
python3 /root/economy_stats/stock_index/src/stock_data.py
echo "2. notion upload"
python3 /root/economy_stats/stock_index/src/notion_upload_stock.py
