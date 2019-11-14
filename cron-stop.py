import schedule
import time
import os

def stopGui():
    print('Stoppping gui')
    os.system("pkill -9 -f gui.py")

schedule.every(150).seconds.do(stopGui)

while True:
    schedule.run_pending()
    time.sleep(1)
