from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .timetable_main import *

def index(request):
    return render(request, 'timetables/index.html')

def senddata(request):
    days = request.POST['days']
    hours = request.POST['hours']
    timetable = compute_timetable(days, hours)

    request.session['days']  = days
    request.session['hours'] = hours
    request.session['timetable'] = timetable.default()

    return HttpResponseRedirect(reverse('timetables:showdata', args=('1A',)))


def showdata(request, groupname):
    return render(request, 'timetables/showdata.html', context={'groupname':groupname})
