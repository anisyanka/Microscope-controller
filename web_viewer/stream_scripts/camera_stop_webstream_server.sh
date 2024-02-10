#!/bin/sh
PID_TO_KILL=`pgrep webstream`

if [ ! -z "${PID_TO_KILL}" ]; then
    echo "kill pid=$PID_TO_KILL"
    kill $PID_TO_KILL > /dev/null
else
    echo "web stream process doesn't exist"
fi
