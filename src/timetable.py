from cell import Cell
import numpy as np
from random import shuffle, randint
from functools import reduce

class TimeTable:

    """ Class to model a timetable of the center """

    """
        Init of the object

     * n_days: how long is the week
     * n_hours:
     * groups: list with all the groups of the center
     * classrooms: list with all the theoretical classrooms of the center
     * practice_classrooms: list with all the practices classrooms of the center
     * semester: describe if the timetable it's for the first semester or the second

    """
    def __init__(self, n_days, n_hours, groups, classrooms, practices_classrooms,
                subjects, semester):
        self.time_table = np.full((n_days, n_hours, len(groups)), fill_value = Cell(), dtype=Cell)
        self.groups = groups
        self.classrooms = classrooms
        self.practices_classrooms = practices_classrooms
        self.subjects = subjects
        self.semester = semester

    def __assign_class__(self, day, hour, subject, group, classroom):
        second_hour = hour + subject.theoretical_hours - 1
        if not (classroom.time_table[day, hour:second_hour]).all():
            self.time_table[day, hour, group] = subject
            classroom.time_table[day, hour:second_hour] = True
            return True
        else:
            return False

    def __get_total_th_hours__(self, subject_list):
        sum = 0
        for i in subject_list:
            sum += i[1].theoretical_hours

        return sum

    def random_greedy(self, semester):
        it = 0
        # for each group
        for group in self.groups.items():

            # we get the subjects and its, theoretical hours
            subject_list =list(filter(lambda x: x[1].year == group[1].year
                                                       and x[1].semester == semester,
                                             self.subjects.items()))
            shuffle(subject_list)
            # day of the week
            day = 0

            while  self.__get_total_th_hours__(subject_list) != 0:
                # for each subject, the algorithm try to assign to an hour
                # the theoretical group.
                for i in range(len(subject_list)):
                    # and only work with the not assign subjects
                    if subject_list[i][1].theoretical_hours > 0:
                        # search the hour
                        for hour in range(self.time_table.shape[1]//2 + 1):
                            # if that hour it's empty, assign the group to that hour
                            if np.all(map(lambda x: x.classroom == group.classroom, self.time_table[hour, day])):

                                self.time_table[hour, day, it] = (group[1].name, group[1].classroom, subject_list[i][1].acronym)
                                subject_list[i][1].theoretical_hours -= 1
                                day = (day + 1) % self.time_table.shape[0]
                                break
            it += 1