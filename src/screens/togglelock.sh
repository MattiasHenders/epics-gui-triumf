
#!/bin/bash

#Sets LOCKNUMBER to the first parameter passed to this bash script
LOCKNUMBER=$1

#Gets the current value of lock{LOCKNUMBER} (1, 2, 3, etc..)
LOCKSTATUS=$(caget lock$LOCKNUMBER) 
LOCKCLOSED=("lock${LOCKNUMBER} CLOSED")

#Strips whitespace from inside LOCKSTATUS string, saves it to STATUS_STRING
STATUS_STRING=$(echo "$LOCKSTATUS" | tr -s " ")

#Inverts the current lock status
if [[ $STATUS_STRING == $LOCKCLOSED ]]; then
caput "lock$LOCKNUMBER" "OPEN"
else
caput "lock$LOCKNUMBER" "CLOSED"
fi

