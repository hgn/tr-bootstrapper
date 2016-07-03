#!/bin/bash

if (( EUID != 0 )); then
	echo "This script must be run as root"
fi

echo "loading sysctl now"
/usr/local/bin/sysctl-loader.sh
