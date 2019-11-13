import bme280;
import smbus2;
import time;
import datetime;
import requests;
import json;
from gtts import gTTS;
import pygame;
from firebase import firebase;

firebase_con = firebase.FirebaseApplication('https://smart-things-2019.firebaseio.com', authentication=None)
authentication = firebase.FirebaseAuthentication('pHkVlRIa1jZMe6VLEyOycXYEd850xDGjiowMDvUy', 'test@gmail.com')
firebase.FirebaseAuthentication = authentication

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

_time = datetime.datetime.now().strftime("%I:%M%p")
date = datetime.datetime.now().strftime("%d/%m/%y")

rq = requests.get('https://extreme-ip-lookup.com/json')
rqdata = json.loads(rq.content.decode())
lat = rqdata['lat']
lon = rqdata['lon']

while True:
    bme280_data = bme280.sample(bus,address)
    hum  = round(bme280_data.humidity,1)
    temp = round(bme280_data.temperature,1)
    
    write_data = {}
    write_data['measurements'] = []
    write_data['measurements'].append({
        'Date': date,
        'Temperature': temp,
        'Humidity': hum
    })    
    with open('data.txt', 'w') as outfile:
        json.dump(write_data, outfile)
    
    with open('data.txt') as json_file:
        read_data = json.load(json_file)
        for p in read_data['measurements']:
            print("{0}: Date: {1}".format(_time, p['Date']))
            print("{0}: Humidity: {1}%".format(_time, p['Humidity']))
            print("{0}: Temperature: {1}C".format(_time, p['Temperature']))
            print("")
            tts = gTTS("The temperature is {0} degrees celcius, with a humidity of {1} percent.".format(p['Temperature'], p['Humidity']), 'en')
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
    firebase_con.put('/0912071-stream-data/sensor-data', "windspeed", 'Heel snel, echt, heb hem net gemeten')
    
    firebase_con.put('/0912071-stream-data/meta-data', "longitude", lon)
    firebase_con.put('/0912071-stream-data/meta-data', "latitude", lat)
    firebase_con.put('/0912071-stream-data/meta-data', "date", date)
    firebase_con.put('/0912071-stream-data/meta-data', "time", _time)
   
    time.sleep(10)
