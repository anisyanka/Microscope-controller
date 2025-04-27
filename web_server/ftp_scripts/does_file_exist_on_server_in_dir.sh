#!/bin/bash

# ret = 0 ==> file exists
# ret = 1 ==> file does NOT exist

# $1 - username
# $2 - userpass
# $3 - ftp server IP
# $4 - ftp server PORT
# $5 - test dir or file
# $6 - where to CWD

testdir=`curl -s --list-only --user "$1:$2" ftp://$3:$4 --quote "CWD $6" | grep $5`

if [ "$5" = "$testdir" ]; then
    exit 0
fi

exit 1
