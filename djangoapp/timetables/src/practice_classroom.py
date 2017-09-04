import numpy as np
from .classroom import ClassRoom
from timetables.models import Classroom
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")
import django
django.setup()
from django.db.models import Q


def create_practice_classroom(filename, days, hours_per_day):
    # Empty list of different classrooms
    classroom = {}
    with open(filename, 'r') as f:
        # Skip the name of the columns
        f.readline()
        # Load data
        for line in f:
            l = line[:-1].split(',')
            materials = set(l[-1].split('-'))
            classroom[l[0]] = PracticeClassRoom(set(map(lambda x: str.upper(x), materials)),
                                                days, hours_per_day, l[0], int(l[1]))

    return classroom

def create_classroom_from_db(days, hours_per_day):
    classes = Classroom.objects.filter(Q(ispractice="Yes") | Q(ispractice="Both")) # retrieve all labs
    classroom = {}
    for c in classes:
        classroom[c.name] = PracticeClassRoom([], days, hours_per_day, c.name, c.capacity)

    return classroom

class PracticeClassRoom (ClassRoom):

    def __init__(self, materials, days, hours_per_day, name, capacity):
        super().__init__(days=days, hours=hours_per_day, name=name, capacity=capacity)
        self.materials = materials
        

    def __repr__(self):
        return self.classroom_name # + " " + str(self.capacity) + " " + str(self.materials)
