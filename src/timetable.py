from cell import Cell
from practice_cell import PracticeCell
import numpy as np
from random import shuffle, randint
from functools import reduce
from itertools import cycle, islice

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
        self.time_table = np.full((len(groups), n_hours, n_days), fill_value = Cell(), dtype=Cell)
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

    def __get_total_th_hours__(self, hour_list):
        totalhours = 0
        for i in hour_list:
            totalhours += i[1]

        return totalhours

    def __assign_cell__(self, group_name, group_classroom, acronym, hour, day, it, subj_name_hours):
        self.time_table[it, hour, day] = Cell(group_name, group_classroom, acronym)
        self.classrooms[group_classroom].time_table[hour,day] = True
        subj_name_hours[acronym] -= 1
        return (day + 1) % self.time_table.shape[2]

    def random_greedy_theory(self, semester):
        it = 0
        # for each group
        for group in self.groups.items():

            # we get the subjects and its, theoretical hours
            subject_list =list(filter(lambda x: x[1].year == group[1].year
                                                       and x[1].semester == semester,
                                             self.subjects.items()))
            shuffle(subject_list)
            subj_name_hours = {subject[0]:subject[1].theoretical_hours for subject in subject_list}
            # day of the week
            day = 0

            while  self.__get_total_th_hours__(subj_name_hours.items()) != 0:
                # print(subj_name_hours)
                # for each subject, the algorithm try to assign to an hour
                # the theoretical group.
                for (name,th_hours) in subj_name_hours.items():
                    # and only work with the not assign subjects
                    if th_hours > 0:
                        # search the hour
                        if group[1].shift == 'M':
                            for hour in range(self.time_table.shape[1]//2):
                                # if that hour it's empty, assign the group to that hour
                                if not self.classrooms[group[1].classroom.classroom_name].time_table[hour,day]:

                                    day = self.__assign_cell__(group[1].name, group[1].classroom.classroom_name, 
                                                               name, hour, day, it, subj_name_hours)

                                    break
                        else:
                            for hour in range(self.time_table.shape[1]//2, self.time_table.shape[1]):
                                # if that hour it's empty, assign the group to that hour
                                if not self.classrooms[group[1].classroom.classroom_name].time_table[hour, day]:

                                    day = self.__assign_cell__(group[1].name, group[1].classroom.classroom_name,
                                                               name, hour, day, it, subj_name_hours)
                                    break

            it += 1

    def __get_total_lab_hours__(self, hour_list):
        totalhours = 0
        for i in hour_list:
            totalhours += sum(i[1])

        return totalhours

    def __assign_lab_cell__(self, window, it, hour, day, group_name, subj_name_hours):
        self.time_table[it, hour, day] = PracticeCell(group_name, subjects=window)
        for (s, i) in zip(window, range(self.groups[group_name].numsubgroups)):
            subj_name_hours[s.acronym][i] -= 1
        return (day + 1) % self.time_table.shape[2]

    def random_greedy_practice(self, semester):
        it = 0

        for group in self.groups.items():
            # get subjects and its practical hours
            subject_list = list(filter(lambda x: x[1].year == group[1].year and
                                                 x[1].semester == semester,
                                                 self.subjects.items()))
            shuffle(subject_list)
            # number of lab hours for each subgroup
            subj_name_hours = {s[0]:[s[1].practical_hours for i in \
                              range(group[1].numsubgroups)] for s in subject_list}
            day = 0

            # create a window of size group.numsubgroups
            # In [4]: a
            # Out[4]: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
            # In [5]: c = [i[1] for i in a.items()]
            # In [5]: b = [tuple(c[i:i+n]) for i in range(len(a)-(n-1))]
            # In [6]: b
            # Out[6]: [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7), (6, 7, 8)]
            aux = [i[1] for i in subject_list]
            aux_cycle = list(islice(cycle(aux), len(aux)+group[1].numsubgroups))

            windows = [aux_cycle[i:i+group[1].numsubgroups] for i in \
                        range(len(aux))]

            while self.__get_total_lab_hours__(subj_name_hours.items()) != 0:
                for window in windows:
                    if sum([subj_name_hours[w.acronym][i] for (w,i) in \
                            zip(window, range(group[1].numsubgroups))]) > 0:

                        if group[1].shift == 'M':
                            for hour in range(self.time_table.shape[1]//2):
                                day = self.__assign_lab_cell__(window, it, hour,
                                    day, group[0], subj_name_hours)

                        else:
                            for hour in range(self.time_table.shape[1]//2, self.time_table.shape[1]):
                                day = self.__assign_lab_cell__(window, it, hour,
                                    day, group[0], subj_name_hours)
                    print(self.time_table)
            it += 1


