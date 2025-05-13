#!/bin/bash

# Return string "<dir_to_create> <file_to_tx>".
# Space separated.

cd /home/pi/.microscope/videos
dir=`find . -maxdepth 1 -type d ! -name '.*' -printf '%f\n' | sort | head -1`
count_of_dirs=`find . -maxdepth 1 -type d ! -name '.*' -printf '%f\n' | sort | wc -l`

# if $dir is a directory
if [ -d "$dir" ]; then
    cd $dir
    files_count=`ls -p | grep -v / | wc -l`

    # Remove local directory if empty
    if [ $files_count -eq 0 ]; then
        cd ..
        rm -rf $dir
        echo "null null"
        exit
    fi

    # Files count > 1
    if [ $files_count -gt 1 ]; then
        file_to_tx=`ls -p | grep -v / | head -1`
        echo "$dir $file_to_tx"
        exit
    else # files == 1. Last one in the dir
        # If NOT last dir
        if [ $count_of_dirs -gt 1 ]; then
            file_to_tx=`ls -p | grep -v / | head -1`
            echo "$dir $file_to_tx"
            exit
        else
            # It is the last file in the last dir. Just return 0 and wait for a new files
            echo "null null"
            exit
        fi
    fi
else
    echo "null null"
    exit
fi
