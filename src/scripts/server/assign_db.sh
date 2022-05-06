#!/bin/bash

echo $1 $2
source ../database/IOC/IOC_DEVICE_ASSOCIATIONS

IOC_TYPE=${!2}
TARGET_IOC=$1
IOC_ID_UPDATE=$2
echo $IOC_TYPE
#Get the IP address of  PV $2
echo "Determining IOC IP Address..."
IP=$(echo $(cainfo $TARGET_IOC:device) | grep Host: | grep -Pom 1 '[0-9.]{7,15}')
echo "Configuring IOC at IP: $IP"

echo "Pushing config to IOC"
#Copy the corresponding IOC db to a generic named file 'dbconfig.db'
cp ../database/IOC/${IOC_TYPE} ../database/dbconfig.db

#Opens a secure transfer ssh connection to transfer the dbconfig.db file
sshpass -p "esado" scp ../database/dbconfig.db esado@${IP}:~

#Opens a ssh connection to kill the current IOC, change the IOC_ID on the IOC device and re-run the IOC
sshpass -p "esado" ssh -t esado@${IP} "pkill screen; sed -i 's/ID=${TARGET_IOC}/ID=${IOC_ID_UPDATE}/' ~/env/IOC_CONFIG && screen -d -m sh -c '/opt/epics/epics-base/bin/linux-x86_64/softIoc -m IOC=${IOC_ID_UPDATE} -d dbconfig.db; exec bash'"
