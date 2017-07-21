from cell import Cell
from practice_cell import PracticeCell
import numpy as np
from random import shuffle, randint, random
from functools import reduce
from itertools import takewhile, dropwhile
from subject import Subject
from itertools import tee

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
        self.is_lab_hour = np.full((len(groups), n_hours, n_days), fill_value='E', dtype=str) # empty
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

    def __get_subj_list__(self, group, semester):
        return list(filter(lambda x: x.year == group.year and x.semester == semester, self.subjects.values()))

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
    Auxiliar function to iterate a list in pairs
    """
    def __pairwise__(self, iterable):
        "s -> (s0,s1) (s1,s2) (s2,s3),..."
        a, b = tee(iterable)
        next (b, None)
        return zip(a,b)

    """
    Function to know the number of theory and lab hours for a given group
    """
    def __group_hours__(self, group, semester):
        # get subject list
        subject_list = self.__get_subj_list__(group, semester)
        # sum lab and theory hours
        lab_hours = sum([s.practical_hours for s in subject_list])
        th_hours  = sum([s.theoretical_hours for s in subject_list])

        return th_hours, lab_hours


    """
    Function to decide which are theory hours and lab hours for each pair of groups.
    """
    def asign_hours(self, semester):
        # variable to iterate through the timetable
        it = 0
        # first, we compute lab/th hours for the 1st goup
        th_hours, lab_hours = self.__group_hours__(list(self.groups.values())[0], semester)
        for hour in range(0, self.is_lab_hour.shape[1] // 2, 2):
            for day in range(self.is_lab_hour.shape[2]):
                if lab_hours > 0:
                    self.is_lab_hour[it, hour, day] = 'L'
                    self.is_lab_hour[it, hour+1, day] = 'L'
                    lab_hours -= 2
                elif th_hours > 0:
                    self.is_lab_hour[it, hour, day] = 'T'
                    self.is_lab_hour[it, hour+1, day] = 'T'
                    th_hours -= 2

        # iterate through all groups in pairs
        for g in list(self.groups.values())[1:]:

            th_hours, lab_hours = self.__group_hours__(g, semester)
            it += 1

            if g.shift == 'M':
                start_range, end_range = 0, self.time_table.shape[1] // 2

            else:
                start_range, end_range = self.time_table.shape[1] // 2, self.time_table.shape[1]

            for hour in range(start_range, end_range, 2):
                for day in range(self.is_lab_hour.shape[2]):
                    if self.is_lab_hour[it-1, hour, day] == 'T' and lab_hours >= 2:
                        self.is_lab_hour[it, hour, day] = 'L'
                        self.is_lab_hour[it, hour+1, day] = 'L'
                        lab_hours -= 2
                    elif self.is_lab_hour[it-1, hour, day] == 'L' and th_hours >= 2: # aquí para el jueves
                        self.is_lab_hour[it, hour, day] = 'T'
                        self.is_lab_hour[it, hour + 1, day] = 'T'
                        th_hours -= 2
                    elif lab_hours >= 2:
                        self.is_lab_hour[it, hour, day] = 'L'
                        self.is_lab_hour[it, hour+1, day] = 'L'
                        lab_hours -= 2
                    elif th_hours >= 2: # aquí para la segunda hora del jueves
                        self.is_lab_hour[it, hour, day] = 'T'
                        self.is_lab_hour[it, hour+1, day] = 'T'
                        th_hours -= 2
                    elif th_hours > 0:
                        if self.is_lab_hour[it,hour,day] == 'E':
                            self.is_lab_hour[it,hour,day] = 'T'
                        elif self.is_lab_hour[it,hour-1,day] == 'E':
                            self.is_lab_hour[it,hour-1,day] = 'T'
                        else:
                            self.is_lab_hour[it,hour+1,day] = 'T'
                        th_hours -= 1
                    elif lab_hours > 0:
                        if self.is_lab_hour[it,hour,day] == 'E':
                            self.is_lab_hour[it,hour,day] = 'L'
                        elif self.is_lab_hour[it,hour-1,day] == 'E':
                            self.is_lab_hour[it,hour-1,day] = 'L'
                        else:
                            self.is_lab_hour[it,hour+1,day] = 'L'
                        lab_hours -= 1
                    else:
                        break


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


            hours_year[year] = th_ph_hours
            year += 1

        return hours_year


    def preassignate_hour_by_year(self):
        pass
