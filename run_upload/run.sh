#!/bin/bash

echo "change the auth src"
chmod 777 ./src

## main logic

echo "1. setup"
python3 ./src/1.setup.py
echo "2. get data"
python3 ./src/2.get.py
echo "3. draw image"
python3 ./src/3.draw.py
echo "4. upload to notion"
python3 ./src/4.upload.py
echo "5. mail report"
python3 ./src/5.mail.py