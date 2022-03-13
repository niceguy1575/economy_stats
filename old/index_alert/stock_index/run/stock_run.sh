#!/bin/bash

eval "$(conda shell.bash hook)"
conda activate economy

echo "change the auth src"
chmod 777 ../src

echo "0. check and install pakcages."
python3 ../src/check_and_install_packages.py
echo "1. get stock data"
python3 ../src/stock_data.py
echo "2. notion upload"
python3 ../src/notion_upload_stock.py

conda deactivate