import bme280;
import RPi.GPIO as GPIO;
import math;
import smbus2;
import time;
import datetime;
import requests;
import json;
from gtts import gTTS;
import pygame;
from firebase import firebase;

GPIO.setmode(GPIO.BCM)
Trig = 23
Echo = 15
Trig2 = 24
Echo2 = 14

GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)
GPIO.setup(Trig2, GPIO.OUT)
GPIO.setup(Echo2, GPIO.IN)

port = 1
address = 0x76
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

firebase_con = firebase.FirebaseApplication('https://smart-things-2019.firebaseio.com', authentication=None)
authentication = firebase.FirebaseAuthentication('pHkVlRIa1jZMe6VLEyOycXYEd850xDGjiowMDvUy', 'test@gmail.com')
firebase.FirebaseAuthentication = authentication

sound_time = 0.095 / 343

def removeSound(speed):
        return speed - sound_time

_time = datetime.datetime.now().strftime("%H:%M")
date = datetime.datetime.now().strftime("%d/%m/%y")

def getWindspeed():
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
    windspeed = round(distance * 1255, 2)
    return windspeed

rq = requests.get('https://extreme-ip-lookup.com/json')
rqdata = json.loads(rq.content.decode())
lat = rqdata['lat']
lon = rqdata['lon']

dataCount = 1

def DataFile():
    global dataCount
    currentCount = dataCount
    if currentCount >= 5:
        dataCount = 1
        return 'data5.txt'
    else:
        dataCount = dataCount + 1
        return "data{0}.txt".format(currentCount)

while True:
    print('Starting at {0}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
    bme280_data = bme280.sample(bus,address)
    wind = getWindspeed()
    hum  = round(bme280_data.humidity,1)
    temp = round(bme280_data.temperature,1)
    _time = datetime.datetime.now().strftime("%H:%M")

    loopFile = DataFile()
    write_data = {}
    write_data['measurements'] = []
    write_data['measurements'].append({
        'Time': _time,
        'Date': date,
        'Temperature': temp,
        'Humidity': hum,
        'Windspeed': wind
    })
    with open(loopFile, 'w') as outfile:
        json.dump(write_data, outfile)

    with open(loopFile) as json_file:
        read_data = json.load(json_file)
        for p in read_data['measurements']:
            print("{0}: Date: {1}".format(_time, p['Date']))
            print("{0}: Humidity: {1}%".format(_time, p['Humidity']))
            print("{0}: Temperature: {1}C".format(_time, p['Temperature']))
            print("{0}: Windspeed: {1}KM/h".format(_time, p['Windspeed']))
            print("")
            if p['Windspeed'] >= 5:
               tts = gTTS("The temperature is {0} degrees celcius, with a humidity of {1} percent. At the moment it's quite windy with speeds up to {2} kilometers per hour".format(p['Temperature'], p['Humidity'], p['Windspeed']), 'en')
            else:
               tts = gTTS("The temperature is {0} degrees celcius, with a humidity of {1} percent. At the moment it's windless with speeds up to {2} kilometers per hour".format(p['Temperature'], p['Humidity'], p['Windspeed']), 'en')
            tts.save('test.mp3')
            pygame.mixer.init()
            pygame.mixer.music.load("test.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue

    firebase_con.put('/0912071-stream-data/student-data', "first-name", 'Guus')
    firebase_con.put('/0912071-stream-data/student-data', "last-name", 'Ekkelenkamp')
    firebase_con.put('/0912071-stream-data/student-data', "student-number", '0912071')
    firebase_con.put('/0912071-stream-data/student-data', "website", 'guusekkelenkamp.nl')

    firebase_con.put('/0912071-stream-data/sensor-data', "humidity", "{0}%".format(hum) )
    firebase_con.put('/0912071-stream-data/sensor-data', "temperature", "{0}°C".format(temp))
    firebase_con.put('/0912071-stream-data/sensor-data', "windspeed", '{0} KM/H'.format(wind))

    firebase_con.put('/0912071-stream-data/meta-data', "longitude", lon)
    firebase_con.put('/0912071-stream-data/meta-data', "latitude", lat)
    firebase_con.put('/0912071-stream-data/meta-data', "date", date)
    firebase_con.put('/0912071-stream-data/meta-data', "time", _time)

    print('Done at {0}'.format(datetime.datetime.now().strftime("%H:%M:%S")))
    time.sleep(270)
