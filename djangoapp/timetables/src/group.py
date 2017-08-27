import numpy as np
from os import environ
from timetables.models import Groups
environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")
import django
django.setup()

def create_group(filename, classroom_list):
    groups = {}
    with open(filename, 'r') as f:
        # skip the name of the columns
        f.readline()
        # load data
        for line in f:
            l = line[:-1].split(',')
            semesters = map(lambda x: int(x), l[-1].split('-'))
            groups[l[0]] = Group(l[0], l[1], int(l[2]),int(l[3]),
                                classroom_list[l[4]],l[5],l[6], semesters)

    return groups

def create_group_from_db(classroom_list):
    group = {}
    groups = Groups.objects.all()
    for g in groups:
        semesters = map(int, g.semester.split(','))
        group[g.name] = Group(g.name, g.shift, g.year, g.numsubgroups, 
                              classroom_list[g.classroom.name], g.degree, 
                              g.speciality, semesters)
    return group

class Group:

    """ Class to model a group of students """

    def __init__(self, name, shift, year, numsubgroups, classroom, 
                 degree, speciality, semester):
        self.shift = shift
        self.year = year
        self.numsubgroups = numsubgroups
        self.classroom = classroom
        self.degree = degree
        self.name = name
        self.speciality = speciality
        self.semester = semester

    def __repr__(self):
        return self.name + " " + self.shift + " " + str(self.year) + " " + \
               str(self.numsubgroups) + " " + str(self.classroom.classroom_name) \
                + " " + self.degree + " " + self.speciality


    def create_subgroups(self):
        pass
