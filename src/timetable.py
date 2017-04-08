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

    def random_greedy(self, semester):
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