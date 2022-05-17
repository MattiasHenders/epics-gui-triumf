#!/bin/bash

source ./env/IOC_CONFIG

echo "Attempting IOC Startup with ID: ${ID}"

PV_LIST=./env/PV_LIST
PVS=`cat $PV_LIST`
IS_RUNNING=$(echo $(pgrep softIoc))
status=$(/opt/epics/epics-base/bin/linux-arm/caget "${ID}:status.INAV")
status_sub=${status: -2}

if [ -z $IS_RUNNING ]
then
	if [ $status_sub == "NC" ]
	then
        	echo "Starting IOC with ID: ${ID}"
        	screen -d -m sh -c "python ~/run_script.py && softIoc -m IOC=${ID} -d dbconfig.db; exec bash"
	else
        	for IOC_PV in $PVS
        	do
                	if [ ! $IOC_PV == $ID ]
                	then
                        	status=$(caget "${IOC_PV}:status.INAV")
                        	status_sub=${status: -2}
                        	if [ $status_sub == "NC" ]
                        	then
                                	echo $IOC_PV
                                	sed -i 's/ID=${ID}/ID=${IOC_PV}/' ~/env/IOC_CONFIG
                                	echo "Starting deviceless IOC with ID: ${IOC_PV}"
                                	echo ${IOC_PV}
                                	screen -d -m sh -c "python ~/run_script.py && softIoc -m IOC=${IOC_PV} -d ND_IOC.db; exec bash"
					break
                        	fi
                	fi
        	done
	fi
fi
