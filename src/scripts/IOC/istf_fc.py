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
    pvID = "ISTF:FC0"

previousList = []

####################################################
# EDIT PVS and GPIO pins HERE 

# PVs Used IN ORDER OF GPIO_LIST
pv0 = PV(pvID + ":SOL")
pv1 = PV(pvID + ":IN")
pv2 = PV(pvID + ":OUT")
pv3 = PV(pvID + ":HWR")

pvList= [pv0.pvname, pv1.pvname, pv2.pvname, pv3.pvname] # List of PVs in order for this device
gpioList = [5, 6, 13, 19]    # List of GPIO pins for this device
gpioOutputList = [True, False, False, True] # False if INPUT / True if Output

#########################
# Callback Functions for PV/GPIO logic
def checkBinarySensor(pv, index):
    
    pin = gpioList[index]
    boolPinOn = (GPIO.input(pin) == GPIO.HIGH)
    
    if boolPinOn != previousList[index]:
        pv.put((0, 1)[boolPinOn])

def SOLPVChanged(pvname=None, value=None, char_value=None, **kw):
    
    boolTurnON = (value == 1)
    index = pvList.index(pvname)

    #Check status of HWR to check if flowing
    boolHWRFlowing = (pv3.get() == 1)

    if not boolHWRFlowing and boolTurnON: 
        print(pvname + ": Change Detected - Water NOT Flowing")
        print(" > Not turning on SOL, Turn On Water First")
        controlGPIO(gpioList[index], False)
        Thread(target=turnOffSOL).start()
        

    elif boolHWRFlowing and boolTurnON:
        print(pvname, ": Change Detected - Water IS Flowing")
        print(" > Turning on SOL!")
        controlGPIO(gpioList[index], True)

    else:
        print(pvname, ": Change Detected - Turning OFF")
        controlGPIO(gpioList[index], False)

def HWRPVChanged(pvname=None, value=None, char_value=None, **kw):
    
    boolTurnON = (value == 1)
    index = pvList.index(pvname)

    #Check status of SOL to check if on
    boolSOLOn = (pv0.get() == 1)

    if boolSOLOn and not boolTurnON: 
        print(pvname + ": Change Detected - Water NOT Flowing")
        print(" > Turning OFF SOL for Safety")
        Thread(target=turnOffSOL).start()

    elif not boolSOLOn and not boolTurnON:
        print(pvname + ": Change Detected - Turning OFF")

    else:
        print(pvname, ": Change Detected - Turning ON")

    controlGPIO(gpioList[index], boolTurnON)

def setup():

    GPIO.setmode(GPIO.BCM)

    for i in gpioList:
        GPIO.setup(i, (GPIO.IN, GPIO.OUT)[gpioOutputList[i]])
        if gpioOutputList[i]:
            GPIO.output(i, GPIO.HIGH)
        previousList.append(False)
    ####################################################
    # SET the interlock devices and interlocks
    
    pv0.add_callback(SOLPVChanged)
    pv3.add_callback(HWRPVChanged)

# BE CAREFUL EDITING PAST HERE! 
####################################################
def turnOffSOL():
    pv0.put(0)

def controlGPIO(GPIO_Pin, boolStatus):
    if not boolStatus:
        GPIO.output(GPIO_Pin, GPIO.HIGH)
    else:
        GPIO.output(GPIO_Pin, GPIO.LOW)

def loop():
    try:
        while True:
            
            # Check for changes to the binary sensors
            checkBinarySensor(pv1, 1)
            checkBinarySensor(pv2, 2)

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