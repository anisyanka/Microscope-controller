#!/bin/sh
for pid in $(lsof -iTCP -sTCP:LISTEN | grep 5000 | awk -F' ' '{print $2}'); do kill -9 $pid 2>/dev/null; done