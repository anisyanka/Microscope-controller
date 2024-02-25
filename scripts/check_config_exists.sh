#!/bin/sh
conf_file=$1

if [ ! -f $1 ]
then
    echo "$4 config NOT FOUND! --> Install default"
    cp $2 $3
else
    echo "$4 config EXISTS! --> Don't copy default"
fi
