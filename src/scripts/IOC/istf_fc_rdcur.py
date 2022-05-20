import sys
from epics import PV
import time
import RPi.GPIO as GPIO
from ADCDevice import *

# Sleep time variables
sleepTimeShort = 0.25
sleepTimeLong = 0.75

# ADC variables
adc = ADCDevice() # Define an ADCDevice class object

# ID From System args
pvID = ""
try:
    pvID = str(sys.argv[1])
except:
    pvID = "ISTF:FC0:RDCUR"


####################################################
# EDIT PVS and GPIO pins HERE 

# PVs Used IN ORDER OF GPIO_LIST
pv0 = PV(pvID)

pvList= [] # List of PVs in order for this device
gpioList = []    # List of GPIO pins for this device

#########################
# Callback Functions for PV/GPIO logic
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

    for i in gpioList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)

    ####################################################
    # SET the interlock devices and interlocks
    
# BE CAREFUL EDITING PAST HERE! 
####################################################

def controlGPIO(GPIO_Pin, boolStatus):
    if not boolStatus:
        GPIO.output(GPIO_Pin, GPIO.HIGH)
    else:
        GPIO.output(GPIO_Pin, GPIO.LOW)

def checkAnalogSensor(pv):
    
    value = adc.analogRead(0)    # read the ADC value of channel 0
    voltage = value / 255.0 * 3.3  # calculate the voltage value
    pv.put(voltage) # Write voltage to EPICS:


def loop():
    try:
        while True:
            
            # Write the voltage to EPICS 
            checkAnalogSensor(pv0)

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