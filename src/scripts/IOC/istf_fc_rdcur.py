import sys
from epics import PV
import time
import RPi.GPIO as GPIO
import spidev

#Define Variables
delay = 0.5
ldr_channel = 0

#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)

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
gpioList = [5]

# PVs Used IN ORDER OF GPIO_LIST
pv0 = PV("ISTF:FC" + pvID + ":RDCUR")
pvList= [pv0]

def setup():

    GPIO.setmode(GPIO.BCM)

    for i in gpioList:
        GPIO.setup(i, GPIO.IN)

def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def loop():
    try:
        while True:

            # Read from the ADC
            ldr_value = readadc(ldr_channel)
            print("LDR Value: %d" % ldr_value)
                
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