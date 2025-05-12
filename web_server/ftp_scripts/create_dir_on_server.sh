#!/bin/bash

# ret = 0 ==> created
# ret = !0 ==> failed to create (might ve already exists)

# $1 - username
# $2 - userpass
# $3 - ftp server IP
# $4 - ftp server PORT
# $5 - dir to create

curl -s --user "$1:$2" ftp://$3:$4 --quote "MKD $5" > /dev/null
ok=$?
echo -n $ok
exit $ok

