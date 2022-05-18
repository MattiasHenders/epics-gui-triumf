import sys
from epics import PV
import time
import RPi.GPIO as GPIO
from threading import Thread

# Sleep time variables
sleepTimeShort = 0.25
sleepTimeLong = 0.75

# ID From System args
pvID = ""
try:
    pvID = str(sys.argv[1])
except:
    pvID = "ISTF:TP0"

####################################################
# EDIT PVS and GPIO pins HERE 

# PVs Used IN ORDER OF GPIO_LIST
pv0 = PV(pvID + ":RP")
pv1 = PV(pvID + ":TP")
pv2 = PV(pvID + ":VV")

pvList= [pv0.pvname, pv1.pvname, pv2.pvname] # List of PVs in order for this device
gpioList = [5, 6, 13]     # List of GPIO pins for this device

#########################
# Callback Functions for PV/GPIO logic
def binaryPVChanged(pvname=None, value=None, char_value=None, **kw):
    
    boolTurnON = (value == 1)
    index = pvList.index(pvname)

    if not boolTurnON: 
        print(pvname + ": Change Detected - Setting OFF")
    else:
        print(pvname + ": Change Detected - Setting ON")

    controlGPIO(gpioList[index], boolTurnON)

def setup():

    GPIO.setmode(GPIO.BCM)

    for i in gpioList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)

    ####################################################
    # SET the interlock devices and interlocks
    
    pv0.add_callback(binaryPVChanged)
    pv1.add_callback(binaryPVChanged)
    pv2.add_callback(binaryPVChanged)

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