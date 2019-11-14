import RPi.GPIO as GPIO
import time
import math
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Trig1 = 24
Trig2 = 23
Echo1 = 15
Echo2 = 14

print("Testing towers")

GPIO.setup(Trig1, GPIO.OUT)
GPIO.setup(Trig2, GPIO.OUT)
GPIO.setup(Echo1, GPIO.IN)
GPIO.setup(Echo2, GPIO.IN)

sound_time = 0.00095 / 343

def removeSound(speed):
        return speed - sound_time

GPIO.output(Trig1, False)
GPIO.output(Trig2, False)
print("Wainting for sensor")
time.sleep(2)

print("Sending pulse 1")
GPIO.output(Trig1, True)
time.sleep(0.00001)
GPIO.output(Trig1, False)

while GPIO.input(Echo1)==0:
    start_timeX = time.time()

while GPIO.input(Echo1)==1:
    end_timeX = time.time()

timeX = removeSound(end_timeX - start_timeX)

print("Waiting for sensor 2")
time.sleep(2)

print("Sending pulse 2")
GPIO.output(Trig2, True)
time.sleep(0.00001)
GPIO.output(Trig2, False)

while GPIO.input(Echo2)==0:
       start_timeY = time.time()

while GPIO.input(Echo1)==1:
        end_timeY = time.time()

timeY = removeSound(end_timeY - start_timeY)
#timeY = removeSound(0.00037872352600098)

distanceX = timeX * timeX
distanceY = timeY * timeY

print(timeX * 1255, "KM/H")
print(timeY * 1255, "KM/H")

distance = math.sqrt(distanceX + distanceY)

print(distance * 1255, "KM/H")
GPIO.cleanup()


def removeSound(speed):
    return speed - sound_time
