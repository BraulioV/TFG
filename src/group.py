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
            groups[l[0]] = Group(l[1],l[2],int(l[3]),int(l[4]),classroom_list[l[5]])

    return groups

class Group:

    """ Class to model a group of students """

    def __init__(self, starttime, endtime, year, numsubgroups, classroom, degree):
        self.starttime = starttime
        self.endtime = endtime
        self.year = year
        self.numsubgroups = numsubgroups
        self.classroom = classroom
        self.degree = degree

    def __repr__(self):
        return str(self.starttime) + " " + str(self.endtime) + " " + str(self.year) + " " \
                + str(self.numsubgroups) + " " + str(self.classroom.classroom_name)


    def create_subgroups(self):
        pass
