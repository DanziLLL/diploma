#!/bin/bash


if [[ $(id -u) != 0 ]]; then
	echo Please run me with sudo!
	exit 1
fi

version=$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ "${version:0:1}" -ne "3" ]]
then
    echo "No compatible Python installed!"
fi

mkdir -p /opt/scripts/inventory_app

. /etc/os-release
case $ID in
    ubuntu|debian)
        FA_VERSION=2.4-2
        apt update
        apt install -y python3-pip
    ;;
    centos)
        yum install python34-setuptools
        easy_install-3.4 pip
    ;;
    fedora)
        dnf install -y python3-pip
    ;;
esac


pip install virtualenv
python3 -m venv /opt/scripts/inventory_app/venv
cp requirements.txt /opt/scripts/inventory_app/
cp *.py /opt/scripts/inventory_app/
cp inventory.sh /opt/scripts/inventory_app/
cd /opt/scripts/inventory_app
chmod +x inventory.sh
source venv/bin/activate
pip install -r requirements.txt
echo "* * * * * sh /opt/scripts/inventory_app/inventory.sh" > /etc/cron.d/inventory
