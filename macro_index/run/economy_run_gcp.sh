#!/bin/bash
echo "change the auth src"
chmod 777 /root/economy_stats_macro_index/src
echo "0. check and install pakcages."
python3 /root/economy_stats/macro_index/src/check_and_install_packages.py
echo "1. get data"
python3 /root/economy_stats/macro_index/src/fred.py
echo "2. get image"
python3 /root/economy_stats/macro_index/src/other_img.py
echo "3. make stats"
python3 /root/economy_stats/macro_index/src/stat.py
echo "4. upload to notion"
python3 /root/economy_stats/macro_index/src/notion_upload.py
