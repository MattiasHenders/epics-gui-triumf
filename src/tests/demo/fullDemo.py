import sys
from epics import PV
import time
import RPi.GPIO as GPIO
from ADCDevice import *
from threading import Thread

# Sleep time variables
sleepTimeShort = 0.25
sleepTimeLong = 0.75

# Safety variables
ledPin = 19       # define ledPin
buttonPin = 13    # define buttonPin
ledState = True

# ID From System args
pvID = ""
try:
    pvID = str(sys.argv[1])
except:
    pvID = "DEMO"

# Global variables
previousList = []
adc = ADCDevice() # Define an ADCDevice class object

####################################################
# EDIT PVS and GPIO pins HERE 

# PVs Used IN ORDER OF GPIO_LIST
pv0 = PV(pvID + ":PWR")
pv1 = PV(pvID + ":SAFETY")
pv2 = PV(pvID + ":VOLTAGE")

pvList= [pv0.pvname] # List of PVs in order for this device
gpioList = [26]    # List of GPIO pins for this device
gpioOutputList = [True] # False if INPUT / True if Output

#########################
# Callback Functions for PV/GPIO logic

def checkAnalogSensor(pv):
    
    value = adc.analogRead(0)    # read the ADC value of channel 0
    voltage = value / 255.0 * 3.3  # calculate the voltage value
    pv.put(voltage) # Write voltage to EPICS

def buttonEvent(channel): # When button is pressed, this function will be executed
    
    global ledState 
    ledState = not ledState

    if ledState:
        Thread(target=turnOnSafety).start()
    else:
        Thread(target=turnOffSafety).start()

    controlGPIO(ledPin, ledState)

def PWRPVChanged(pvname=None, value=None, char_value=None, **kw):
    
    boolTurnON = (value == 1)
    index = pvList.index(pvname)

    #Check status of HWR to check if flowing
    boolSafetyON = (pv1.get() == 1)

    if not boolSafetyON and boolTurnON: 
        print(pvname + ": Change Detected - Safety OFF")
        print(" > Not turning on PWR, Turn On Safety")
        controlGPIO(gpioList[index], False)
        Thread(target=turnOffPWR).start()
        

    elif boolSafetyON and boolTurnON:
        print(pvname, ": Change Detected - Safety ON")
        print(" > Turning on PWR!")
        controlGPIO(gpioList[index], True)

    else:
        print(pvname, ": Change Detected - Turning OFF")
        controlGPIO(gpioList[index], False)

def SafetyPVChanged(pvname=None, value=None, char_value=None, **kw):
    
    boolTurnON = (value == 1)
    global ledState
    ledState = boolTurnON
    
    if not boolTurnON: 
        print(pvname + ": Change Detected - Safety OFF")
        print(" > Turning OFF PWR to be safe.")
        controlGPIO(ledPin, False)
        Thread(target=turnOffPWR).start()

    else:
        print(pvname + ": Change Detected - Safety ON")
        controlGPIO(ledPin, True)

def setup():

    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)

    GPIO.setmode(GPIO.BCM)

    for i in range(len(gpioList)):
        
        GPIO.setup(gpioList[i], (GPIO.IN, GPIO.OUT)[gpioOutputList[i]])

        if gpioOutputList[i]:
            GPIO.output(gpioList[i], GPIO.LOW)
        previousList.append(False)

    GPIO.setup(ledPin, GPIO.OUT)     # set ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.HIGH)

    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set buttonPin to PULL UP INPUT mode

    ####################################################
    # SET the interlock devices and interlocks
    
    pv0.add_callback(PWRPVChanged)
    pv1.add_callback(SafetyPVChanged)

# BE CAREFUL EDITING PAST HERE! 
####################################################
def turnOffPWR():
    pv0.put(0)

def turnOffSafety():
    pv1.put(0)

def turnOnSafety():
    pv1.put(1)

def controlGPIO(GPIO_Pin, boolStatus):
    if not boolStatus:
        GPIO.output(GPIO_Pin, GPIO.LOW)
    else:
        GPIO.output(GPIO_Pin, GPIO.HIGH)

def loop():
    try:

        GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback = buttonEvent,bouncetime=300)

        while True:

            # Check the analog sensors
            checkAnalogSensor(pv2)

            # Wait a short amount of secs
            time.sleep(sleepTimeShort)

    # End program cleanly with keyboard
    except KeyboardInterrupt:
        print("Quit via user interupt")

        # Reset ADC
        adc.close()

        # Reset GPIO settings
        GPIO.cleanup()

        

def main():
    setup()
    loop()

# Run the main
main()