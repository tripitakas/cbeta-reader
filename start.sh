#!/bin/sh
kill -9 `ps -ef | grep 8001 | grep main.py | awk -F" " {'print $2'}` 2>/dev/null
cd `dirname $0`
find `dirname $0` -name "*.pyc" | xargs rm -rf
nohup python3 main.py --port=8001 --debug=false >> log/app.log 2>&1 &
