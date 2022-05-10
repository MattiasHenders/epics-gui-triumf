#!/bin/bash

source ./env/IOC_CONFIG

echo "Starting IOC with ID: ${ID}"

screen -d -m softIoc -m IOC=${ID} -d dbconfig.db




