#!/bin/sh

make uninstall
git pull origin master
make
make install
