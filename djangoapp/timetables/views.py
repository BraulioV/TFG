from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
import sys

def index(request):
    return render(request, 'timetables/index.html')

def senddata(request):
    print("fghhgdgh", file=sys.stderr)
    # if request.method == 'POST':
    days = request.POST['days']
    hours = request.POST['hours']

    return HttpResponseRedirect(reverse('timetables:showdata', args=(days, hours,)))
    # else:
    #     return render(request, 'timetables/index.html')


def showdata(request, days, hours):
    return render(request, 'timetables/showdata.html', {'days':days, 'hours':hours})