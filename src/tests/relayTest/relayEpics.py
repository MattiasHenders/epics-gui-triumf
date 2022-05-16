import RPi.GPIO as GPIO
import time
import epics

gpioList = [6, 13, 19, 26]
gpioBool = [False, False, False, False]
timeSleepShort = 0.25
timeSleepLong = 1

def setup():

    GPIO.setmode(GPIO.BCM)

    for i in gpioList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)

def loop():

    prevLED = False

    try:
        while True:
            
            checkRelay(1)
            checkRelay(2)
            checkRelay(3)
            checkRelay(4)
            
            time.sleep(timeSleepLong)

    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()

def checkRelay(num):
    
    boolRelay = epics.caget('relay%d' %num) == 1
    
    if (gpioBool[num - 1] != boolRelay):
                
        if(boolRelay):
            GPIO.output(gpioList[num - 1], GPIO.LOW)  # make ledPin output HIGH level to turn on led
            print ('relay %d turned on >>>' %num)     # print information on terminal
        else:
            GPIO.output(gpioList[num - 1], GPIO.HIGH)   # make ledPin output LOW level to turn off led
            print ('relay %d turned off <<<' %num)
            
        gpioBool[num - 1] = boolRelay

def main():
    setup()
    loop()

main()
            

