import bme280
import smbus2
import time;
import datetime;
import json

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

date_time = datetime.datetime.now().strftime("%I:%M%p")

while True:
    bme280_data = bme280.sample(bus,address)
    hum  = round(bme280_data.humidity,1)
    temp = round(bme280_data.temperature,1)
    #print("{0}: Humudity: {1}%".format(date_time, hum))
    #print("{0}: Temperature: {1}°C".format(date_time, temp))
    data = {}
    data['measurements'] = []
    data['measurements'].append({
        'Temperature': temp,
        'Humidity': hum
    })    
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
    time.sleep(10)
    
