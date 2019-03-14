from django.shortcuts import render
from django.http import HttpResponse
from .models import Sensordata

import datetime
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


# Create your views here.
def index(request):
    data = Sensordata.objects.all()

    return render(request, "data.html", {"data": data})

def lineplot(request, sensor):

    fig=Figure()
    fig.suptitle(sensor)
    ax=fig.add_subplot(111)
    data = Sensordata.objects.all()[4:]
    x = data.values_list("date", flat=True)
    y = data.values_list(sensor, flat=True)
    print(x)
    print(y)

    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%m.%d %H'))
    fig.autofmt_xdate()

    buf = io.BytesIO()
    canvas=FigureCanvas(fig)
    canvas.print_png(buf)
    response=HttpResponse(buf.getvalue(), content_type='image/png')
    return response

def histogram(request, sensor):

    fig=Figure()
    fig.suptitle(sensor)
    ax=fig.add_subplot(111)
    data = Sensordata.objects.all()[4:]
    x = data.values_list(sensor, flat=True)

    ax.hist(x, bins=15)

    buf = io.BytesIO()
    canvas=FigureCanvas(fig)
    canvas.print_png(buf)
    response=HttpResponse(buf.getvalue(), content_type='image/png')
    return response
