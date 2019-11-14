import RPi.GPIO as GPIO
import time
import math
GPIO.setmode(GPIO.BCM)

Trig = 23
Echo = 15
Trig2 = 24
Echo2 = 14

GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)
GPIO.setup(Trig2, GPIO.OUT)
GPIO.setup(Echo2, GPIO.IN)

sound_time = 0.095 / 343

def removeSound(speed):
        return speed - sound_time

GPIO.output(Trig, False)
time.sleep(2)

GPIO.output(Trig, True)
time.sleep(0.00001)
GPIO.output(Trig, False)

while GPIO.input(Echo)==0:
    start = time.time()

while GPIO.input(Echo)==1:
    end = time.time()

time.sleep(3)
duration = removeSound(end - start)

GPIO.output(Trig2, False)
time.sleep(2)

GPIO.output(Trig2, True)
time.sleep(0.00001)
GPIO.output(Trig2, False)

while GPIO.input(Echo2)==0:
    start2 = time.time()

while GPIO.input(Echo2)==1:
    end2 = time.time()
    
time.sleep(3)
duration2 = removeSound(end2 - start2)

distanceX = duration * duration
distanceY = duration2 * duration2
distance = math.sqrt(distanceX + distanceY)
windspeed = round(distance * 1255,2)
print(windspeed, "KM/H")

GPIO.cleanup()
