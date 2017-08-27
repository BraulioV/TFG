from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .timetable_main import *

def index(request):
    return render(request, 'timetables/index.html')

def senddata(request):
    days = request.POST['days']
    hours = request.POST['hours']

    return HttpResponseRedirect(reverse('timetables:showdata', args=(days, hours,)))


def showdata(request, days, hours):
    prepare_data(days, hours)
    return render(request, 'timetables/showdata.html', {'days':days, 'hours':hours})
