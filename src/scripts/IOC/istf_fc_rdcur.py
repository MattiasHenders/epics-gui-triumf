import sys
from epics import PV
import time
import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Sleep time variables
sleepTimeShort = 0.25
sleepTimeLong = 0.75

# ADC variables
# Create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# Create the cs (chip select) NOTE: D5 is the GPIO Pin we are reading from  
cs = digitalio.DigitalInOut(board.D5)
# Create the mcp object
mcp = MCP.MCP3008(spi, cs)
# Create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

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

pvList= [pv0.pvname] # List of PVs in order for this device
gpioList = [5]    # List of GPIO pins for this device

#########################
# Callback Functions for PV/GPIO logic
def setup():

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

def loop():
    try:
        while True:
            
            # Write the voltage to EPICS 
            pv0.put(chan.voltage)

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