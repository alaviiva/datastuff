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
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):
    data = Sensordata.objects.all()

    return render(request, "db.html", {"data": data})

def test(request):

    fig=Figure()
    ax=fig.add_subplot(111)
    data = Sensordata.objects.all()
    x = data.values_list("date", flat=True)
    y = data.values_list("sensor1", flat=True)
    print(x)
    print(y)

    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    buf = io.BytesIO()
    canvas=FigureCanvas(fig)
    canvas.print_png(buf)
    response=HttpResponse(buf.getvalue(), content_type='image/png')
    return response
