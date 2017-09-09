import re
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .timetable_main import *
from .models import Groups

def index(request):
    return render(request, 'timetables/index.html')

def senddata(request):
    input_val = re.compile('^\d')
    if not input_val.match(request.POST['days']) and \
       not input_val.match(request.POST['hours']) and \
       not input_val.match(request.POST['semester']):
       raise ValidationError("Incorrect input format")

    days = int(request.POST['days'])
    hours = int(request.POST['hours'])
    semester = int(request.POST['semester'])

    if (hours - days) > 5:
        raise ValidationError("It is physically imposible to make a timetable " +
            "with such a little number of hours.")

    if days < 4 or days > 5:
        raise ValidationError("Specify a valid number of days")

    if hours < 10 or hours > 13:
        raise ValidationError("Specify a valid number of hours")

    timetable = compute_timetable(days, hours, semester)

    request.session['days']  = days
    request.session['hours'] = hours
    request.session['semester'] = semester
    request.session['full_timetable'] = timetable.dict_timetable()

    return HttpResponseRedirect(reverse('timetables:showdata', args=('1A',)))


def showdata(request, groupname):
    request.session['timetable']    = request.session['full_timetable'][groupname]
    request.session['numsubgroups'] = Groups.objects.get(name=groupname).numsubgroups

    return render(request, 'timetables/showdata.html', context={'groupname':groupname})

def pdf(request):
    make_pdf(request.session['full_timetable'], request.session['days'], request.session['hours'], request.session['semester'])
    with open('timetables/src/resources/Outputs/prueba.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=prueba.pdf'
        return response
