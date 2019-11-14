import threading
import sys
import tkinter as tk
from pandas import DataFrame
from PIL import ImageTk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json

i = 1
_time =[]
tmp = []
hum = []
wind = []

while i < 6:
    with open("data{0}.txt".format(i)) as json_file:
        read_data = json.load(json_file)
        for p in read_data['measurements']:
            _time.append(p['Time'])
            hum.append(p['Humidity'])
            tmp.append(p['Temperature'])
            wind.append(p['Windspeed'])
    i = i+1

Data1 = {'Time': _time,
        'Temperature': tmp
       }

df1 = DataFrame(Data1, columns= ['Time', 'Temperature'])
df1 = df1[['Time', 'Temperature']].groupby('Time').sum()
df1 = df1.sort_values(by=['Time'])

Data2 = {'Time': _time,
        'Humidity': hum
       }

df2 = DataFrame(Data2, columns= ['Time', 'Humidity'])
df2 = df2[['Time', 'Humidity']].groupby('Time').sum()
df2 = df2.sort_values(by=['Time'])

Data3 = {'Time': _time,
        'Windspeed': wind
       }

df3 = DataFrame(Data3, columns= ['Time', 'Windspeed'])
df3 = df3[['Time', 'Windspeed']].groupby('Time').sum()
df3 = df3.sort_values(by=['Time'])

root= tk.Tk()

figure1 = plt.Figure(figsize=(2,2), dpi=133)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df1.plot(kind='bar', legend=False, ax=ax1, fontsize=6)
ax1.set_title('Temperature in °C')

figure2 = plt.Figure(figsize=(2,6), dpi=133)
ax2 = figure2.add_subplot(111)
bar2 = FigureCanvasTkAgg(figure2, root)
bar2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df2.plot(kind='bar', legend=False, ax=ax2, color='g', fontsize=6)
ax2.set_title('Humidity in %')

figure3 = plt.Figure(figsize=(2,2), dpi=133)
ax3 = figure3.add_subplot(111)
bar3 = FigureCanvasTkAgg(figure3, root)
bar3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df3.plot(kind='bar', legend=False, ax=ax3, color='r', fontsize=6)
ax3.set_title('Windspeed in KM/H')

def destroy():
    root.destroy()

#t = threading.Timer(5.0, destroy)
#t.start()

root.mainloop()

#print('out')
#exit()
