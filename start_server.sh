#!/bin/bash

echo "STARTING EPICS SERVER"
## Add HLA startup here ##
pkill screen
screen -d -m sh -c 'cd high-level-application && flask run --host 0.0.0.0'
screen -d -m sh -c 'softIoc -d src/database/server/iocstatus.db; exit'
screen -list
echo "SERVER STARTED"
