#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate economy

echo "change the auth src"
cd /Users/jongwon/python/economy/economy_stats/run_on_mac
chmod 777 ../stock_index/src

echo "0. check and install pakcages."
python3 ../stock_index/src/check_and_install_packages.py
echo "1. get stock data"
python3 ../stock_index/src/stock_data.py
echo "2. notion upload"
python3 ../stock_index/src/notion_upload_stock.py

conda deactivate