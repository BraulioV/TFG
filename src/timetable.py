import numpy as np

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
    def __init__(self, n_days, n_hours, groups, classrooms, practices_classrooms):
        self.time_table = np.zeros((n_days, n_hours, len(groups)))
        self.groups = groups
        self.classrooms = classrooms
        self.practices_classrooms = practices_classrooms