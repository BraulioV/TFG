import numpy as np
from random import choice, randint

class TimeTable:

    """ Class to model a timetable of the center """

    """
        Init of the object

     * n_days: how long is the week
     * n_hours:
     * groups: list with all the groups of the center
     * classrooms: list with all the theoretical classrooms of the center
     * practice_classrooms: list with all the practices classrooms of the center

    """
    def __init__(self, n_days, n_hours, groups, classrooms, practices_classrooms,
                subjects):
        self.time_table = np.zeros((n_days, n_hours, len(groups)))
        self.groups = groups
        self.classrooms = classrooms
        self.practices_classrooms = practices_classrooms
        self.subjects = subjects

    def random_greedy(self):
        for name, classroom in self.classrooms.items():
            # filter groups assigned to that theory class
            group = dict(filter(lambda g: g[1].classroom.classrom_name == name, 
                                self.groups.items()))
            for name, g in group:
                # filter subjects assigned to that group
                subject = dict(filter(lambda s: s[1].year == g.year and 
                                     s[1].speciality == g.speciality, 
                                     self.subjects.items()))

                # assign all subjects theorical hours to random time in the 
                # classroom table
                n_days, n_hours, _ = self.time_table.shape
