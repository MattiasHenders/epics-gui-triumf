#!/bin/bash

echo "STARTING EPICS SERVER"
## Add HLA startup here ##
screen -d -m sh -c 'softIoc -d ../../database/server/iocstatus.db; exit'

