#!/bin/bash

echo "Switching $1 to $2"
#mapfile -t arr ~/epics-gui-triumf/src/database/IOC/IOC_DEVICE_ASSOCIATIONS.txt

IOC_TYPE=""
TARGET_IOC=$1
IOC_ID_UPDATE=$2

# Parses the correct DB file for the IOC we want to re-assign to
while IFS= read -r line; do
elementPV=$(echo $line | cut -d "=" -f 1)
elementDB=$(echo $line | cut -d "=" -f 2)
if [ $elementPV == $IOC_ID_UPDATE ]
then
IOC_TYPE=$elementDB
echo $IOC_TYPE
echo "Switching $2 database to $IOC_TYPE"
fi
done < ~/epics-gui-triumf/src/database/IOC/IOC_DEVICE_ASSOCIATIONS.txt

#Get the IP address of PV $1
echo "Determining IOC IP Address..."
IP=$(echo $(cainfo $TARGET_IOC:device) | grep Host: | grep -Pom 1 '[0-9.]{7,15}')
SCRIPT_DIR=${IOC_TYPE::-2}py
IOC_IN_USE=$(caget $2:status.INAV)

if [ ! -z $IP -a ${IOC_IN_USE: -2} == "NC" ]
then 


echo "Configuring IOC at IP: $IP"
#Copy the corresponding IOC db to a generic named file 'dbconfig.db'
rm -r ~/epics-gui-triumf/src/database/dbconfig.db
rm -r ~/epics-gui-triumf/src/scripts/run_script.py
cp -r ~/epics-gui-triumf/src/database/IOC/${IOC_TYPE} ~/epics-gui-triumf/src/database/dbconfig.db
cp -r ~/epics-gui-triumf/src/scripts/IOC/${SCRIPT_DIR} ~/epics-gui-triumf/src/scripts/run_script.py

echo $IOC_TYPE
#Opens a secure transfer ssh connection to transfer the dbconfig.db file
sshpass -p "triumf" scp ~/epics-gui-triumf/src/database/dbconfig.db pi@${IP}:~
sshpass -p "triumf" scp ~/epics-gui-triumf/src/scripts/run_script.py pi@${IP}:~

echo $IOC_ID_UPDATE
#Opens a ssh connection to kill the current IOC, change the IOC_ID on the IOC device and re-run the IOC
sshpass -p "triumf" ssh -t pi@${IP} "pkill screen; sed -i 's/ID=${TARGET_IOC}/ID=${IOC_ID_UPDATE}/' ~/env/IOC_CONFIG && screen -L -d -m sh -c '/opt/epics/epics-base/bin/linux-arm/softIoc -m IOC=${IOC_ID_UPDATE} -d ~/dbconfig.db; exit' && screen -L -d -m sh -c 'python3 ~/run_script.py ${IOC_ID_UPDATE}; exit'"

else
	echo "RPI with that PV not available!"
fi

