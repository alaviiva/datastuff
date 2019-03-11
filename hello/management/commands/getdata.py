from django.core.management.base import BaseCommand
import os
import requests
from hello.models import Sensordata
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

URL = "https://opendata.hopefully.works/api/events"
TOKEN = os.environ["API_TOKEN"]

class Command(BaseCommand):

    def getdata(self):
        headers = {"Authorization": "Bearer " + TOKEN}

        r = requests.get(URL, headers=headers)
        j = r.json()
        d = datetime.fromisoformat(j["date"][:19]+"+00:00")
        print(d)
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

    def startscheduler(self):
        print("startscheduler")
        scheduler = BlockingScheduler()
        self.getdata()
        scheduler.add_job(self.getdata, 'interval', hours=1)
        scheduler.start()

    def handle(self, *args, **options):
        self.startscheduler()
