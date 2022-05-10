#!/bin/bash

source ./env/IOC_CONFIG

echo "Attempting IOC Startup with ID: ${ID}"

caget "${ID}:status.INAV"
status=$(caget "${ID}:status.INAV")
status_sub=${status: -2}

if [ $status_sub == "NC" ]
then
	echo "Starting IOC with ID: ${ID}"
	screen -d -m softIoc -m IOC=${ID} -d dbconfig.db
else
	for IOC in {1..20}
	do
		if [ ! $IOC == ${ID: -1} ]
		then
			status=$(caget "${IOC}:status.INAV")
			status_sub=${status: -2}
			if [ $status_sub == "NC" ]
			then
				sed -i 's/ID=${ID}/ID=IOC_${$IOC}/' ~/env/IOC_CONFIG
				echo "Starting deviceless IOC with ID: IOC_${ID}"
				screen -d softIoc -m IOC=${ID} -d ND_IOC.db
			fi
		fi
	done
fi




