#!/bin/bash

#echo "activate python3"
#eval "$(conda shell.bash hook)"
#conda activate economy

echo "change the auth src"
cd /Users/jongwon/python/economy/economy_stats/run_on_mac
chmod 777 ../macro_index/src


## main logic
echo "0. check and install pakcages."
python3 ../macro_index/src/check_and_install_packages.py
echo "1. get data"
python3 ../macro_index/src/fred.py
echo "2. get image"
python3 ../macro_index/src/other_img.py
echo "3. make stats"
python3 ../macro_index/src/stat.py
echo "4. upload to notion"
python3 ../macro_index/src/notion_upload.py

#conda deactivate
