#!/bin/bash

echo "activate python3"
eval "$(conda shell.bash hook)"
conda activate economy

echo "change the auth src"
cd /Users/jongwon/python/economy/economy_stats/run_on_mac
chmod 777 ../macro_index/src
chmod 777 ../stock_index/src

## main logic
echo "logic1. macro economy"
python3 ../macro_index/src/check_and_install_packages.py
echo "1-1. get data"
python3 ../macro_index/src/fred.py
echo "1-2. get image"
python3 ../macro_index/src/other_img.py
echo "1-3. make stats"
python3 ../macro_index/src/stat.py
echo "1-4. upload to notion"
python3 ../macro_index/src/notion_upload.py

echo "logic2. stock economy"
python3 ../stock_index/src/check_and_install_packages.py
echo "2-1. get stock data"
python3 ../stock_index/src/stock_data.py
echo "2-2. notion upload"
python3 ../stock_index/src/notion_upload_stock.py



conda deactivate
