#!/bin/bash

if (( EUID != 0 )); then
	echo "This script must be run as root"
fi

sysctl -p /etc/sysctl.d/60-specific.conf 
