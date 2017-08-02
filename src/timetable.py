import random as rd
from cell import Cell
from practice_cell import PracticeCell
import numpy as np
from random import shuffle, randint, random, sample, choices
from functools import reduce
from itertools import takewhile, dropwhile
from subject import Subject
from itertools import tee
from math import ceil

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
     * subjects: dict with all the subjects

    """
    def __init__(self, n_days, n_hours, groups, classrooms, practices_classrooms,
                subjects, semester):
        self.time_table = np.full((len(groups), n_hours, n_days), fill_value = Cell(), dtype=Cell)
        self.structure = np.full((len(groups), n_hours, n_days), fill_value='E', dtype=str) # empty
        self.groups = groups
        self.classrooms = classrooms
        self.practices_classrooms = practices_classrooms
        self.subjects = subjects
        self.semester = semester
        self.possible_pr_classrooms = {}
        self.__get_possible_classrooms__()

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

    def __get_subj_list__(self, group):
        return list(filter(lambda x: x.year == group.year and x.semester == self.semester, self.subjects.values()))

    def __assign_cell__(self, group_name, group_classroom, acronym, hour, day, it, subj_name_hours):
        if subj_name_hours[acronym] >= 2:
            self.time_table[it, hour, day] = Cell(group_name, group_classroom, acronym)
            self.time_table[it, hour+1, day] = Cell(group_name, group_classroom, acronym)
            self.classrooms[group_classroom].time_table[hour,day] = True
            self.classrooms[group_classroom].time_table[hour+1, day] = True
            subj_name_hours[acronym] -= 2
        else:
            self.time_table[it, hour, day] = Cell(group_name, group_classroom, acronym)
            self.classrooms[group_classroom].time_table[hour, day] = True
            subj_name_hours[acronym] -= 1

        return (day + 1) % self.time_table.shape[2]


    def __get_possible_classrooms__(self):

        for subject in self.subjects:

            # Get the necessary materials for that subject
            materials = self.subjects[subject].special_requirements
            # and the possible classrooms where the subject
            # can be taught. A classroom become a possible option
            # if the interesection between it's materials and
            # the subject's materials are equal to the
            # subject's material
            possible_classrooms = list(filter(lambda x:
                                              (self.practices_classrooms[x].materials & materials) == materials,
                                              self.practices_classrooms))

            self.possible_pr_classrooms[subject] = possible_classrooms


    def random_greedy_theory(self, semester):
        it = 0
        # for each group
        plus = 2 if random() < 0.5 else 0
        for group in self.groups.values():

            # we get the subjects and its, theoretical hours
            subject_list =self.__get_subj_list__(group, semester)

            shuffle(subject_list)
            subj_name_hours = {subject.acronym:subject.theoretical_hours for subject in subject_list}
            # day of the week
            day = 0

            if group.shift == 'M':
                start_range, end_range = 0, self.time_table.shape[1] // 2

            else:
                start_range, end_range = self.time_table.shape[1] // 2, self.time_table.shape[1]

            plus = 2 if plus == 0 else 0
            while self.__get_total_th_hours__(subj_name_hours.items()) != 0:
                # print(subj_name_hours)
                # for each subject, the algorithm try to assign to an hour
                # the theoretical group.

                for (name,th_hours) in subj_name_hours.items():
                    # and only work with the not assign subjects

                    if th_hours > 0:

                        # search the hour
                        for hour in range(start_range + plus, end_range):
                            # if that hour it's empty, assign the group to that hour
                            if not self.classrooms[group.classroom.classroom_name].time_table[hour,day]:

                                day = self.__assign_cell__(group.name, group.classroom.classroom_name,
                                                           name, hour, day, it, subj_name_hours)

                                break
            it += 1

    def __get_total_lab_hours__(self, hour_list):
        
        totalhours = 0

        for i in hour_list:
            totalhours += sum(i[1])

        return totalhours

    def __assign_lab_cell__(self, window, it, hour, day, group_name, subj_name_hours):
        local_window = []
        for (w, i) in zip(window, range(len(window))):
            if subj_name_hours[w.acronym][i] > 0:
                local_window.append(w)
            else:
                local_window.append(Subject())

        # si la celda estaba previamente vacía: asignamos la ventana completa
        if self.time_table[it, hour, day] == PracticeCell():

            self.time_table[it, hour, day] = PracticeCell(group_name, subjects=local_window)

            for (s, i) in zip(window, range(self.groups[group_name].numsubgroups)):
                for classroom in self.possible_pr_classrooms[s.acronym]:

                    if not self.practices_classrooms[classroom].time_table[hour, day]:

                        self.practices_classrooms[classroom].time_table[hour, day] = True
                        self.time_table[it, hour, day].classrooms.append(classroom)
                        if subj_name_hours[s.acronym][i] > 0:
                            subj_name_hours[s.acronym][i] -= 1

                        break


        # si la celda NO estaba vacía, sólo podemos asignar los huecos que tenga.
        else:
            # 1. Buscar índices de huecos
            indices = {i for i, x in enumerate(self.time_table[it,hour,day].subjects) if x == Subject()}
            # 2. Buscar índices de huecos de asignaturas
            subj = {w.acronym:[] for w in window if sum(subj_name_hours[w.acronym])}
            for s,l in subj.items():
                for i,x in enumerate(subj_name_hours[s]):
                    if x == 1:
                        l.append(i)

            # 3. Asignar al hueco la asignatura que le corresponda y restar 1
            for s,l in subj.items():
                for h in l:
                    if self.time_table[it,hour,day].subjects[h] == Subject() and subj_name_hours[s][h] > 0:
                        self.time_table[it, hour, day].subjects[h] = self.subjects[s]
                        subj_name_hours[s][h] -= 1

    def random_greedy_practice(self, semester):
        it = -1
        for group in self.groups.items():
            # get subjects and its practical hours
            subject_list = self.__get_subj_list__(group, semester)
            
            shuffle(subject_list)
            sorted(subject_list)
            print(subject_list)
            # number of lab hours for each subgroup
            # subj_name_hours = {s[0]:[s[1].practical_hours for i in \
            #                   range(group[1].numsubgroups)] for s in subject_list}
            # subj_name_hours['']=[0,0,0]
            # day = 0
            #
            # # create a window of size group.numsubgroups
            # # In [4]: a
            # # Out[4]: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
            # # In [5]: c = [i[1] for i in a.items()]
            # # In [5]: b = [tuple(c[i:i+n]) for i in range(len(a)-(n-1))]
            # # In [6]: b
            # # Out[6]: [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7), (6, 7, 8)]
            # aux = [i[1] for i in subject_list]
            # aux_cycle = list(islice(cycle(aux), len(aux)+group[1].numsubgroups))
            #
            # windows = [aux_cycle[i:i+group[1].numsubgroups] for i in \
            #             range(len(aux))]
            # it += 1
            # i=0
            #
            # if group[1].shift == 'M':
            #     start_range, end_range = 0, self.time_table.shape[1] // 2
            #
            # else:
            #     start_range, end_range = self.time_table.shape[1] // 2, self.time_table.shape[1]
            #
            #
            # while self.__get_total_lab_hours__(subj_name_hours.items()) != 0:
            #     while i < len(windows):
            #         window = windows[i]
            #
            #         if sum([subj_name_hours[w.acronym][i] for (w,i) in \
            #                 zip(window, range(group[1].numsubgroups))]) > 0:
            #
            #             for hour in range(start_range, end_range):
            #                 if self.time_table[it, hour, day].is_free(window, subj_name_hours):
            #                     self.__assign_lab_cell__(window, it, hour,
            #                                              day, group[0], subj_name_hours)
            #                     if hour == end_range-1:
            #                         i = (i + 1) % len(windows)
            #
            #         else:
            #             i = (i + 1) % len(windows)
            #             break
            #
            #         day = (day + 1) % self.time_table.shape[2]
            #
            # print(self.time_table)

    """
        Aux function to iterate a list in pairs
    """
    def __pairwise__(self, iterable):
        "s -> (s0,s1) (s1,s2) (s2,s3),..."
        a, b = tee(iterable)
        next (b, None)
        return zip(a,b)

    """
    Function to know the number of theory and lab hours for a given group
    """
    def __group_hours__(self, group):
        # get subject list
        subject_list = self.__get_subj_list__(group)
        # sum lab and theory hours
        if group.speciality == "Troncal":
            lab_hours = sum([s.practical_hours for s in subject_list])
            th_hours  = sum([s.theoretical_hours for s in subject_list])
            return th_hours, lab_hours

        else:
            subject_group = list(filter(lambda x: x.speciality == group.speciality, subject_list))
            group_lab_hours = sum([s.practical_hours for s in subject_group])
            group_th_hours = sum([s.theoretical_hours for s in subject_group])
            return group_th_hours, group_lab_hours

    """
                            Compute total hours
                    
        This function compute the total theoretical hours and practical
        hours for each year of the degree. Returns a dict.
    """
    def compute_total_hours(self):

        hours_year, year = {}, 1

        subjects = self.subjects.items()

        while len(subjects) != 0:
            th_ph_hours = [0,0]
            aux = list(takewhile(lambda x: x[1].year == year, subjects))
            subjects = list(dropwhile(lambda x: x[1].year == year, subjects))

            for subject in aux:
                th_ph_hours[0] += subject[1].theoretical_hours
                th_ph_hours[1] += subject[1].practical_hours


            hours_year[year] = tuple(th_ph_hours)
            year += 1

        return hours_year

    def change_structure(self, it, hour, day, kind):
        self.structure[it, hour, day] = kind
        self.structure[it, hour + 1, day] = kind

    def preassignate_hour_by_year(self, shift):
        # filter groups in given shift
        local_groups = dict(filter(lambda x: x[1].shift == shift, self.groups.items()))

        # compute total theory/lab hours for each year
        hours = self.compute_total_hours()
        n_groups = {}

        # compute total number of groups in given shift
        for year in hours.keys():
            gs = list(filter(lambda x: x.year == year and x.shift == shift, local_groups.values()))
            n_g = len(gs)
            if n_g != 0:
                n_groups[year] = (n_g, gs)

        # compute range of shift
        if shift == 'M':
            start_range, end_range = 0, self.time_table.shape[1] // 2

        else:
            start_range, end_range = self.time_table.shape[1] // 2, self.time_table.shape[1]

        shift_indexes = list(filter(lambda x: x != -1, map(lambda x, y: x if y.shift == shift else -1,
                                 range(len(self.groups.values())), self.groups.values())))

        # split shift_indexes list into sublists that fits the number of groups of each year
        index_years = [[shift_indexes.pop(0) for k in range(i[0])] for i in n_groups.values()]

        # for each year, compute theory/lab distribution
        for hour_aux, groups, years in zip(hours.values(), n_groups.values(), index_years):
            th, lab = hour_aux
            numgroups, grs = groups

            # compute total lab hours of all groups
            total_lab = ceil((lab * numgroups) / 2) # each lab hour is a block of two hours
            # compute total lab hours available in a week
            days_week = self.structure.shape[2]
            total_week = days_week * 2 # total days * total lab hours in a day

            # once computed total lab hours required and total lab hours available, we need to check out if
            # there are more hours needed than available. If so, we need to decide which hours are going to
            # be repeated by choosing a random integer
            if total_lab > total_week:
                rep = choices(range(total_week), k=total_lab - total_week)
                days = list(map(lambda x: (x % 5, start_range if x < 5 else start_range + 2), rep))
            else:
                days = []

                # auxiliar 2D matrix that tells if an hour is lab or not in a whole year.
            is_lab_hour = np.full(self.structure.shape[1:], fill_value=False, dtype=bool)

            # now we iterate in all groups in that year
            for g, it in zip(grs, years):
                th_hours, lab_hours = self.__group_hours__(g)
                for hour in range(start_range, end_range, 2):
                    for day in range(days_week):
                        if not is_lab_hour[hour, day] and lab_hours >= 2:
                            self.change_structure(it, hour, day, 'L')
                            is_lab_hour[hour, day] = True
                            is_lab_hour[hour + 1, day] = True
                            lab_hours -= 2
                        elif is_lab_hour[hour, day] and lab_hours >= 2 and (day, hour) in days:
                            del days[days.index((day, hour))]
                            self.change_structure(it, hour, day, 'L')
                            lab_hours -= 2
                        elif is_lab_hour[hour, day] and th_hours >= 2:
                            self.change_structure(it, hour, day, 'T')
                            th_hours -= 2
                        elif th_hours >= 2:
                            self.change_structure(it, hour, day, 'T')
                            th_hours -= 2
                        elif lab_hours >= 2:
                            self.change_structure(it, hour, day, 'L')
                            lab_hours -= 2
                        else:
                            break