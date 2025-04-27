#!/bin/bash

PID1=`pgrep curl`

if [ ! -z "${PID1}" ]; then
    echo "kill pid=$PID1"
    kill -INT $PID1 > /dev/null
else
    echo "FTP curl transfers don't exist"
fi
