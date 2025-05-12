#!/bin/bash

# ret = 0 ==> file exists
# ret = 1 ==> file does NOT exist

# $1 - username
# $2 - userpass
# $3 - ftp server IP
# $4 - ftp server PORT
# $5 - test dir or file


testdir=`curl -s --list-only --user "$1:$2" ftp://$3:$4 | grep $5`

if [ "$5" = "$testdir" ]; then
    echo -n "0"
    exit 0
fi

echo -n "1"
exit 1
