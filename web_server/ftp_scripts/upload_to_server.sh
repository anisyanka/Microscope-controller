#!/bin/bash

# ret = 0 ==> uploaded
# ret = !0 ==> failed to upload

# $1 - username
# $2 - userpass
# $3 - ftp server IP
# $4 - ftp server PORT
# $5 - filename
# $6 - whereto (если директории нет, то вроде как возвращает число 9)

curl -s --user "$1:$2" -T $5 ftp://$3:$4/$6/
ok=$?

if [ $ok -eq 0 ]; then
    rm -rf $5
fi

echo -n $ok
exit $ok
