import sys
from epics import PV
import time
import RPi.GPIO as GPIO

#Define Variables


# Sleep time variables
sleepTimeShort = 0.25
sleepTimeLong = 0.75

# ID From System args
pvID = ""
try:
    pvID = str(sys.argv[1])
except:
    pvID = "ISTF:FC0:RDCUR"

# List to track previous states
boolPrevList = []

####################################################
# EDIT PVS and GPIO pins HERE 

# PVs Used IN ORDER OF GPIO_LIST
pv0 = PV(pvID)

pvList= [pv0] # List of PVs in order for this device
gpioList = [5] # List of GPIO pins for this device

#Declare which PVs can only be turned on by interlock logic
lockedPVs = []
#########################
# BE CAREFUL EDITING PAST HERE! 
####################################################

def setup():

    GPIO.setmode(GPIO.BCM)

    for i in gpioList:
        GPIO.setup(i, GPIO.IN)
        boolPrevList.append(False)

    ####################################################
    # SET the interlock devices and interlocks

    # BE CAREFUL EDITING PAST HERE! 
    ####################################################

def controlGPIO(GPIO_Pin, boolStatus):
    if not boolStatus:
        GPIO.output(GPIO_Pin, GPIO.HIGH)
    else:
        GPIO.output(GPIO_Pin, GPIO.LOW)

def loop():
    try:
        while True:

            # Loop through each PV
            for i in range(len(gpioList)):

                if pvList[i] in lockedPVs:
                    continue

                # Check the PV value
                boolPV = pvList[i].get() != 0

                # Act only if there is a change
                if boolPrevList[i] != boolPV:
                    controlGPIO(gpioList[i], boolPV)
                    boolPrevList[i] = boolPV
                
            # Wait a short amount of secs
            time.sleep(sleepTimeShort)

    # End program cleanly with keyboard
    except KeyboardInterrupt:
        print("Quit via user interupt")

        # Reset GPIO settings
        GPIO.cleanup()

def main():
    setup()
    loop()

# Run the main
main()