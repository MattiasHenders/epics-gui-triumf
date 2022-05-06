#!/bin/bash

IFS="PV"

while [ 1 ]
do
	sleep 5
	for i in {1..3}
	do
		#echo $i
		IOC_STATUS_STRING=$(caget IOC_${i}:status.INAV)
		IOC_STATUS=${IOC_STATUS_STRING:38:2}
		echo $IOC_STATUS
		if [ "$IOC_STATUS" = "NC" ];
		then
			caput IOC_${i}:status 0
		fi
		
	done
	
done
