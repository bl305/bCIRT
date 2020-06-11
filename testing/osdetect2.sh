#!/bin/bash

#arch=$(uname -m)
#kernel=$(uname -r)
if [ -n "$(command -v lsb_release)" ]; then
	distroname=$(lsb_release -s -d)
elif [ -f "/etc/os-release" ]; then
	distroname=$(grep PRETTY_NAME /etc/os-release | sed 's/PRETTY_NAME=//g' | tr -d '="')
elif [ -f "/etc/debian_version" ]; then
	distroname="Debian $(cat /etc/debian_version)"
elif [ -f "/etc/redhat-release" ]; then
	distroname=$(cat /etc/redhat-release)
else
	distroname="$(uname -s) $(uname -r)"
fi

if [[ $distroname == *"Ubuntu"* ]] || [[ $distroname == *"Debian"* ]]; then
  if [ -f /usr/bin/apt ];then
    echo "apt!"
    osupdates=$(apt list --upgradeable)
  elif [ -f /usr/bin/apt-get ]; then
    echo "apt-get!"
    osupdates=$(apt-get upgrade -s)
  fi
fi
#echo "${distroname}"
echo "${osupdates}"

