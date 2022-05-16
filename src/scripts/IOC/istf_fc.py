import sys
from epics import PV, Alarm
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
    pvID = "0"

# List of GPIO pins for this device
gpioList = [5, 6, 13, 19]

# PVs Used IN ORDER OF GPIO_LIST
pv0 = PV("ISTF:FC" + pvID + ":SOL")
pv1 = PV("ISTF:FC" + pvID + ":IN")
pv2 = PV("ISTF:FC" + pvID + ":OUT")
pv3 = PV("ISTF:FC" + pvID + ":HWR")
pvList= [pv0, pv1, pv2, pv3]

#Declare which PVs can only be turned on by interlock logic
lockedPVs = [pv0]

# List to track previous states
boolPrevList = []
    
# Alarms and callbacks
def turnOnSOL(pvname=None, value=None, char_value=None, **kw):
    print("Change Detected")
    if pv0.get() == 1 and pv1.get() == 0 and pv2.get() == 1:
        print("Turning ON SOL")
        controlGPIO(gpioList[0], True)
    else:
        print("Turning OFF SOL")
        pv0.put(0) # Critical
        controlGPIO(gpioList[0], False)

def setup():

    GPIO.setmode(GPIO.BCM)

    for i in gpioList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)
        boolPrevList.append(False)
    
    # Set the interlock devices change function
    pv0.add_callback(turnOnSOL)
    pv1.add_callback(turnOnSOL)
    pv2.add_callback(turnOnSOL)

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