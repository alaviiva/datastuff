import os
import requests
from .models import Sensordata
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

DATABASE_URL = os.environ['DATABASE_URL']
URL = "https://opendata.hopefully.works/api/events"
TOKEN = os.environ["API_TOKEN"]

def getdata():
    headers = {"Authorization": "Bearer " + TOKEN}

    r = requests.get(URL, headers=headers)
    j = r.json()
    date = datetime.fromisoformat(j["date"][:19])
    

    data = Sensordata()
    data.date = date
    data.sensor1=j["sensor1"]
    data.sensor2=j["sensor2"]
    data.sensor3=j["sensor3"]
    data.sensor4=j["sensor4"]
    #data.save()

    print("update", j)

def startscheduler():
    print("startscheduler")
    scheduler = BackgroundScheduler()
    #getdata()
    scheduler.add_job(getdata, 'interval', minutes=1)
    scheduler.start()
