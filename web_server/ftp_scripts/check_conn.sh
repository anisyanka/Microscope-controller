#!/bin/bash

# ret = 0 ==> connection OK!
# ret = 7 ==> server not running or wrong IP:PORT
# ret = 67 ==> failed to login; check user and pass

# $1 - username
# $2 - userpass
# $3 - ftp server IP
# $4 - ftp server PORT

conn=`curl -s --list-only --user "$1:$2" ftp://$3:$4 > /dev/null`
exit $conn


