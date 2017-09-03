import numpy as np
from timetables.models import Classroom
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")
import django
django.setup()
from django.db.models import Q


def create_classroom_from_csv(filename, days, hours_per_day):
    # Empty list of different classrooms
    classroom = {}
    with open(filename, 'r') as f:
        # Skip the name of the columns
        f.readline()
        # Load data
        for line in f:
            l = line[:-1].split(',')
            classroom[l[0]] = ClassRoom(days, hours_per_day, l[0], int(l[1]))

    return classroom

def create_classroom_from_db(days, hours_per_day):
    classes = Classroom.objects.filter(Q(ispractice="No") | Q(ispractice="Both")) # retrieve all theory classes
    classroom = {}
    for c in classes:
        classroom[c.name] = ClassRoom(days, hours_per_day, c.name, c.capacity)

    return classroom

class ClassRoom:

    """ Class to model a classroom for a specific bachelor """

    def __init__(self, days, hours, name, capacity):
        self.time_table = np.full((hours, days), fill_value=False)
        self.capacity = capacity
        self.classroom_name = name

    def __repr__(self):
        return str(self.capacity) + " " + self.classroom_name

    """ Fill a specific hour a classroom """

    def assign_class(self, x, y, group, subject):
        # If time_table[x,y] is empty, assign the
        # group and the subject
        if not self.time_table[x,y]:
            self.time_table[x,y] = [group, subject]
            return True

        return False

    def delete_at(self, x, y):
        self.time_table[x, y] = False
