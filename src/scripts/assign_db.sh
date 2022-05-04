#!/bin/bash

echo $1 $2 $3

IOC_CONFIG=$1
TARGET_IOC=$2
IOC_ID_UPDATE=$3

#Get the IP address of  PV $2
echo "Determining IOC IP Address..."
IP=$(echo $(cainfo $2:device) | grep Host: | grep -Pom 1 '[0-9.]{7,15}')
echo $IP

echo "Pushing config to IOC"
cp ../database/IOC/${1} ../database/dbconfig.db
sshpass -p "raspberry" scp ../database/dbconfig.db pi@${IP}:~

ssh pi@${IP} "sudo sed -i 's/ID=${2}/ID=${3}/' ~/sshTesting/env/IOC_CONFIG ; pkill softIoc ; setsid ~/sshTesting/start_script.sh &"
#ssh pi@${IP} "sudo pkill softIoc"
