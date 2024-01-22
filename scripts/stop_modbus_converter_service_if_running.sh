
if systemctl is-active --quiet $1 ; then
    echo "$1 is running, so stop it"
    sudo systemctl disable $1
	sudo systemctl stop $1
else
    echo "$1 is inactive"
fi
