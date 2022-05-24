#!/bin/bash

source /home/pi/env/IOC_CONFIG

echo "Attempting IOC Startup with ID: ${ID}"

PV_LIST=./env/PV_LIST
PVS=`cat $PV_LIST`
IS_RUNNING=$(echo $(pgrep softIoc))
status=$(/opt/epics/epics-base/bin/linux-arm/caget "${ID}:status.INAV")
status_sub=${status: -2}

#If this RPI is not already serving an IOC then try to start one using this RPI's IOC ID
if [ -z $IS_RUNNING ]
then

#If the ID that this IOC is trying to serve does not already have a connection then start this IOC
	if [ $status_sub == "NC" ]
	then
        	echo "Starting IOC with ID: ${ID}"

#Creates two screens that run a softIoc and our python script in background ubuntu sessions
        	/usr/bin/screen -d -m sh -c "softIoc -m IOC=${ID} -d dbconfig.db; exec bash"
                /usr/bin/screen -d -m sh -c "python ~/run_script.py ${ID}; exec bash"
	else

#Otherwise assign this IOC as an ND_IOC using the PV_LIST file
        	for IOC_PV in $PVS
        	do

#If the currently iterated IOC_PV is not equal to this RPIs ID, check that IOC_PV is not being served by another IOC
                	if [ ! $IOC_PV == $ID ]
                	then
                        	status=$(caget "${IOC_PV}:status.INAV")
                        	status_sub=${status: -2}

#If IOC_PV is not already being served on the network, start the IOC with that ND_IOC ID
                        	if [ $status_sub == "NC" ]
                        	then
                                	echo $IOC_PV
                                	sed -i 's/ID=${ID}/ID=${IOC_PV}/' ~/env/IOC_CONFIG
                                	echo "Starting deviceless IOC with ID: ${IOC_PV}"
                                	/usr/bin/screen -d -m sh -c "softIoc -m IOC=${IOC_PV} -d ND_IOC.db; exec bash"
                                        /usr/bin/screen -d -m sh -c "python ~/run_script.py ${IOC_PV}; exec bash"
					break
                        	fi
                	fi
        	done
	fi
fi
