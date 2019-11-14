import schedule
import time
import os

def startGui():
    print('Starting gui')
    os.system("python3 gui.py 1")

schedule.every(1).seconds.do(startGui)

while True:
    schedule.run_pending()
    time.sleep(1)
