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
        self.time_table = np.zeros((n_days, n_hours, len(groups)), dtype=str)
        self.groups = groups
        self.classrooms = classrooms
        self.practices_classrooms = practices_classrooms
        self.subjects = subjects

    def __assign_class__(self, day, hour, subject, group, classroom):
        second_hour = hour + subject.theoretical_hours - 1
        if not (classroom.time_table[day, hour:second_hour]).all():
            self.time_table[day, hour, group] = subject
            classroom.time_table[day, hour:second_hour] = True
            return True
        else:
            return False


    def random_greedy(self):
        for cname, classroom in self.classrooms.items():
            # filter groups assigned to that theory class
            group = dict(filter(lambda g: g[1].classroom.classroom_name == cname, 
                                self.groups.items()))
            for gname, g in group.items():
                group_index = list(self.groups.keys()).index(gname)
                # filter subjects assigned to that group
                subject = dict(filter(lambda s: s[1].year == g.year and 
                                     s[1].speciality == g.speciality, 
                                     self.subjects.items()))


                # assign all subjects theorical hours to random time in the 
                # classroom table
                n_days, n_hours, _ = self.time_table.shape
                for d in range(n_days):
                    if not subject:
                        break
                    if g.franja == "M":
                        for h in range(n_hours//2):
                            if not subject:
                                break
                            s = choice(list(subject.items()))
                            is_assigned = self.__assign_class__(d, h, s[1], \
                                group_index, classroom)
                            if is_assigned:
                                del subject[s[0]]

                    else: # g.franja == "T"
                        for h in range(n_hours//2, n_hours):
                            if not subject:
                                break
                            s = choice(list(subject.items()))
                            is_assigned = self.__assign_class__(d, h, s[1], \
                                group_index, classroom)
                            if is_assigned:
                                del subject[s[0]]
