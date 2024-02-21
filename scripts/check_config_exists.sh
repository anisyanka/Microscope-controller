#!/bin/sh
conf_file=$1

if [ ! -f $1 ]
then
    echo
    echo "$4 config NOT FOUND! --> Install default"
    cp $2 $3
    echo
else
    echo
    echo "$4 config EXISTS! --> Don't copy default"
    echo
fi
