import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

gpioList = [6, 13, 19, 26]

for i in gpioList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

sleepTimeShort = 0.25
sleepTimeLong = 0.75

try:
    while True:
        for i in gpioList:
            GPIO.output(i, GPIO.LOW)
            time.sleep(sleepTimeShort)
            GPIO.output(i, GPIO.HIGH)
            time.sleep(sleepTimeLong)

except KeyboardInterrupt:
    print("Quit")
    
    GPIO.cleanup()

            
