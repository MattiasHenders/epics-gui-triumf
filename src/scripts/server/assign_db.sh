#!/bin/bash

echo $1 $2
source ../database/IOC/IOC_DEVICE_ASSOCIATIONS

IOC_TYPE=${!2}
TARGET_IOC=$1
IOC_ID_UPDATE=$2
echo $2
echo $IOC_TYPE
#Get the IP address of PV $1
echo "Determining IOC IP Address..."
IP=$(echo $(cainfo $TARGET_IOC:device) | grep Host: | grep -Pom 1 '[0-9.]{7,15}')
SCRIPT_DIR=${IOC_TYPE::-2}py
IOC_IN_USE=$(caget $2:status.INAV)
echo ${IOC_IN_USE: -2}
echo ${IP}
if [ ! -z $IP -a ${IOC_IN_USE: -2} == "NC" ]
then 


echo "Configuring IOC at IP: $IP"
#Copy the corresponding IOC db to a generic named file 'dbconfig.db'
cp ../database/IOC/${IOC_TYPE} ../database/dbconfig.db
cp ../scripts/IOC/${SCRIPT_DIR} ../scripts/run_script.py

#Opens a secure transfer ssh connection to transfer the dbconfig.db file
sshpass -p "triumf" scp StrictHostKeyChecking=no ../database/dbconfig.db pi@${IP}:~
sshpass -p "triumf" scp StrictHostKeyChecking=no ../scripts/run_script.py pi@${IP}:~

#Opens a ssh connection to kill the current IOC, change the IOC_ID on the IOC device and re-run the IOC
sshpass -p "triumf" ssh -t StrictHostKeyChecking=no pi@${IP} "pkill screen; sed -i 's/ID=${TARGET_IOC}/ID=${IOC_ID_UPDATE}/' ~/env/IOC_CONFIG && screen -d -m sh -c '/opt/epics/epics-base/bin/linux-arm/softIoc -m IOC=${IOC_ID_UPDATE} -d dbconfig.db; python ~/run_script.py; exec bash'"

else
	echo "RPI with that PV not available!"
fi

