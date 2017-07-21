import numpy as np
import sub_group

def create_group(filename, classroom_list):
    groups = {}
    with open(filename, 'r') as f:
        # skip the name of the columns
        f.readline()
        # load data
        for line in f:
            l = line[:-1].split(',')
            semesters = l[-1].split('-')
            groups[l[0]] = Group(l[0], l[1], int(l[2]),int(l[3]),
                                classroom_list[l[4]],l[5],l[6], semesters)

    return groups

class Group:

    """ Class to model a group of students """

    def __init__(self, name, franja, year, numsubgroups, classroom, 
                 degree, speciality, semester):
        self.shift = franja
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
