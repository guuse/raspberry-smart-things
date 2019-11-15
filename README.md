# The project
For this project i've created a homestation which collects Windspeed, Temperature and Humidity. I've also created a GUI with 3 graphs that show the measurements.
For the temperature and humidty im using a BME280 sensor. For the windspeed I've used 4 ultrasonic sensors.
I'm using a 7" raspberry pi display to show off my graphs/measurements.

#How to run
Make sure to set up your circuit https://drive.google.com/file/d/1KlBjhFupi4Uf5oshehENlncN494vS39o/view?usp=sharing

Install all modules listed in the `req.txt` folder, this can be done by running `pip3 install --no-cache-dir -r req.txt`

Navigate to the project folder and run `pyhton3 main_script.py`

Open a new tab and run `cron-start.py`

Open a new tab and run `cron-stop.py`

You should see a GUI with data from the main script

#Explanation
This project uses 2 main scripts, and 2 cron-like scripts.

### main_script.py
This script is the brain of the whole project. 
All measurements, API calls and calculations happen inside this script. 
The script can be split into 6 parts; Setup, Location, Windspeed, Data parsing, Sound & firebase.
The script is set up in an infinite loop, on a timer of 5 minutes. 
Which means every 5 minutes new data gets parsed and send to the database.

###### Setup:
The setup is initiated with setting all the GPIO pins and settings correctly.
The pins used for my ultrasonic sensors are 14, 15, 23 & 24.
The BME280 needs to be setp up via IC2. 
**The adress may vary from pi to pi here.**
The BME280 get calibrated and is ready for use.
The last thing we need to setup is our firebase conection, which is done next.

###### Location:
For our location, we do an api call to: `https://extreme-ip-lookup.com/json`.
This returns alot of information about our IP adress in JSON format.
This information also contains our Latitude and Longitude.
We store these values in 2 variables.

###### Windspeed:
We use ultrasonic sensors to measure our windspeed. 
The 4 sensors are setup in a cross formation, with a sender and reciever opposite of eachother.
We first need to get the time it takes for the wave to get from the sender to reciever.
We use EPOCH timestamps from time sent to time received.
We subtract the received time from the sent time to get the duration of the wave.
We then remove the speed of sound over 9.5 cm (the distance between sender and reciever) to get the windspeed in 1 direction.

We do the exact same thing for the other sender and reciever.

We now have an X and Y windspeed. 
We use pythagoras to get the total windspeed.
We multiple the number by 1255 to convert the distance to KM/H.
We then return the value.

###### data parsing:
We first make a function that can check in what loop count we are.
We do this because we want our GUI to collect data from the 5 latest measurements. 
We then collect the data from the windspeed function and BME280, and put that as json in a text file.
We then open our text file and read the data and print in on the command line.
**(This can be done with the vars aswell, but I used this to practice getting json data from txt files)**


###### Sound:
With all the data we have, we use the Google TTS module to write to an mp3 file.
We create an if statement around the windspeed, so we have two possible outputs.
We then use a different module to read out this mp3 file, and play it on the PI.
We have an external speaker hooked up to our PI and set it up so this mp3 will always play to this speaker.


###### Firebase:
Finally we need to send our data to the firebase database.
The firebase PUT method gets used for this.
We send all our data to the correct endpoints and the script is then completed.


### gui.py
This script creates a GUI which plots our 5 most recent measurements on a graph.

It starts by creating 4 different arrays.
An array for time, temprature, humidity and windspeed.
We read out json from our txt files (created by the main script), and append them to our arrays.
We then create 3 different dataframes, for our sensor data.
We link our measurements to the proper time.
When our datasets are ready, we can start creating our GUI.
We use TKinter to create a GUI for our measurements.
We create 3 bar graphs, and plot our dataset on them accordingly.
We place the graphs next to eachother with 3 different colors.
Then we start our mainloop, which starts our GUI.


### cron-start.py & cron-stop.py
Becuase our graphs are not live graphs, we have to refresh our data plotted on them.
I thought of the idea to create 2 cron-like scripts. One which starts our script (when not running) every second.
And one which closes it every 2.5 minutes.
This way our measurements get replotted every 2.5 minutes. And it provides our graph with a "fake" refresh.
