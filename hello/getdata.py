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
    d = datetime.fromisoformat(j["date"][:19])
    if (Sensordata.objects.filter(date=d).count() > 0):
        print("nothing new")
        return False

    data = Sensordata()
    data.date = d
    data.sensor1=j["sensor1"]
    data.sensor2=j["sensor2"]
    data.sensor3=j["sensor3"]
    data.sensor4=j["sensor4"]
    data.save()

    print("update", j)
    return True

def startscheduler():
    print("startscheduler")
    scheduler = BackgroundScheduler()
    #getdata()
    scheduler.add_job(getdata, 'interval', hours=1)
    scheduler.start()
