import sys
from epics import PV
import time
import RPi.GPIO as GPIO

# Sleep time variables
sleepTimeShort = 0.25
sleepTimeLong = 0.75

# ID From System args
pvID = ""
try:
    pvID = str(sys.argv[1])
except:
    pvID = "ISTF:GV0"

previousList = []

####################################################
# EDIT PVS and GPIO pins HERE 

# PVs Used IN ORDER OF GPIO_LIST
pv0 = PV(pvID + ":SOL")
pv1 = PV(pvID + ":IN")
pv2 = PV(pvID + ":OUT")

pvList= [pv0, pv1, pv2] # List of PVs in order for this device
gpioList = [5, 6, 13]   # List of GPIO pins for this device
gpioOutputList = [True, False, False] # False if INPUT / True if Output

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

    for i in range(len(gpioList)):
        GPIO.setup(gpioList[i], (GPIO.IN, GPIO.OUT)[gpioOutputList[i]])
        if gpioOutputList[i]:
            GPIO.output(gpioList[i], GPIO.HIGH)
        previousList.append(False)
    ####################################################
    # SET the interlock devices and interlocks
    
    pv0.add_callback(binaryPVChanged)

# BE CAREFUL EDITING PAST HERE! 
####################################################

def controlGPIO(GPIO_Pin, boolStatus):
    if not boolStatus:
        GPIO.output(GPIO_Pin, GPIO.HIGH)
    else:
        GPIO.output(GPIO_Pin, GPIO.LOW)

def checkBinarySensor(pv, index):
    
    pin = gpioList[index]
    boolPinOn = (GPIO.input(pin) == GPIO.HIGH)
    
    if boolPinOn != previousList[index]:
        pv.put((0, 1)[boolPinOn])

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