#!/bin/bash

echo "1. get data"
python3 ../src/fred.py
echo "2. get image"
python3 ../src/other_img.py
echo "3. make stats"
python3 ../src/stat.py
echo "4. upload to notion"
python3 ../src/notion_upload.py