#!/bin/bash

echo $1 $2
source ../database/IOC/IOC_DEVICE_ASSOCIATIONS

IOC_TYPE=${!1}
TARGET_IOC=$1

#Get the IP address of PV $1
echo "Determining IOC IP Address..."
IP=$(echo $(cainfo $TARGET_IOC:device) | grep Host: | grep -Pom 1 '[0-9.]{7,15}')
SCRIPT_DIR=${IOC_TYPE::-2}py

if [ ! -z $IP ]
then


echo "Configuring IOC at IP: $IP"
#Copy the corresponding IOC db to a generic named file 'dbconfig.db'
cp ../database/IOC/${IOC_TYPE} ../database/dbconfig.db
cp ../scripts/IOC/${SCRIPT_DIR} ../scripts/run_script.py

#Opens a secure transfer ssh connection to transfer the dbconfig.db file
sshpass -p "triumf" scp ../database/dbconfig.db pi@${IP}:~
sshpass -p "triumf" scp ../scripts/run_script.py pi@${IP}:~

#Opens a ssh connection to kill the current IOC, change the IOC_ID on the IOC device and re-run the IOC
sshpass -p "triumf" ssh -t pi@${IP} "pkill screen; ~/env/IOC_CONFIG  && screen -d -m sh -c '~/EPICS/epics-base/bin/linux-arm/softIoc -m IOC=${TARGET_IOC} -d dbconfig.db; python ~/run_script.py; exec bash'"
else
        echo "RPI with that PV not available!"
fi
