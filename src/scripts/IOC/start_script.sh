#!/bin/bash

source ./env/IOC_CONFIG

PV_LIST=./env/PV_LIST
PVS=`cat $PV_LIST`

echo "Attempting IOC Startup with ID: ${ID}"

caget "${ID}:status.INAV"
status=$(caget "${ID}:status.INAV")
status_sub=${status: -2}

if [ $status_sub == "NC" ]
then
	echo "Starting IOC with ID: ${ID}"
	screen -d -m softIoc -m IOC=${ID} -d dbconfig.db
else
	for IOC_PV in $PVS
	do
		if [ ! $IOC_PV == $ID ]
		then
			status=$(caget "${IOC_PV}:status.INAV")
			status_sub=${status: -2}
			if [ $status_sub == "NC" ]
			then
				sed -i 's/ID=${ID}/ID=${$IOC_PV}/' ~/env/IOC_CONFIG
				echo "Starting deviceless IOC with ID: ${ID}"
				screen -d softIoc -m IOC=${ID} -d ND_IOC.db
			fi
		fi
	done
fi




