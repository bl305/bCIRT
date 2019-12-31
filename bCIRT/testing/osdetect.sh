#!/bin/bash
aID=$(awk -F= '/^ID=/{print $2}' /etc/*release)
aVER=$(awk -F= '/^VERSION_ID=/{print $2}' /etc/*release)
#cat /etc/*release | grep "^VERSION_ID="
echo $aID $aVER
