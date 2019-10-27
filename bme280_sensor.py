import bme280
import smbus2
import time;
import datetime;
import json;
from firebase import firebase

firebase_con = firebase.FirebaseApplication('https://smart-things-2019.firebaseio.com', authentication=None)
authentication = firebase.FirebaseAuthentication('pHkVlRIa1jZMe6VLEyOycXYEd850xDGjiowMDvUy', 'test@gmail.com')
firebase.FirebaseAuthentication = authentication

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

_time = datetime.datetime.now().strftime("%I:%M%p")
date = datetime.datetime.now().strftime("%d/%m/%y")

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
            print("{0}: Temperature: {1}°C".format(_time, p['Temperature']))
            print(bme280_data.pressure)
            print("")

    new_user = 'Test gebruiker'
    #firebase_con.post('/users', new_user)
    #result = firebase_con.get('/users', None)
    #print(result)
    
    time.sleep(1)
