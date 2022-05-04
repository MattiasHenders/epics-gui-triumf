#!/bin/bash

source ./env/IOC_CONFIG

echo "Starting IOC with ID: ${ID}"

(softIoc -m IOC=$ID -d dbconfig.db)





