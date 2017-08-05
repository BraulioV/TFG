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
        self.groups = dict(filter(lambda g: semester in g[1].semester, groups.items()))
        self.classrooms = classrooms
        self.practices_classrooms = practices_classrooms
        self.subjects = dict(filter(lambda s: s[1].semester == semester, subjects.items()))
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
        return list(filter(lambda x: x.year == group.year, self.subjects.values()))


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


    def random_greedy_theory(self):
        for group, it in zip(self.groups.values(), range(self.time_table.shape[0])):
            # we get the subjects and its, theoretical hours
            subject_list =self.__get_subj_list__(group)

            shuffle(subject_list)
            subj_name_hours = {subject.acronym:subject.theoretical_hours for subject in subject_list}
            s = 0

            if group.shift == 'M':
                start_range, end_range = 0, self.time_table.shape[1] // 2

            else:
                start_range, end_range = self.time_table.shape[1] // 2, self.time_table.shape[1]


            for h in range(start_range, end_range, 2):
                for d in range(self.time_table.shape[2]):

                    # 1st case: this hour is assigned to lab/is empty
                    if (self.structure[it,h,d] == 'L' or self.structure[it,h,d] == 'E') \
                            and self.structure[it, h+1, d] != 'T':
                        pass

                    # 2nd case: this hour is assigned to theory and we can make a 2 hours block with actual
                    # subject in s.
                    elif self.structure[it,h,d] == 'T' and subj_name_hours[subject_list[s].acronym] >= 2\
                            and self.time_table[it,h,d] == Cell() and self.time_table[it,h+1,d] == Cell():
                        self.time_table[it,h,d] = Cell(group.name, group.classroom.classroom_name,
                                                       subject_list[s].acronym)
                        self.time_table[it, h+1, d] = Cell(group.name, group.classroom.classroom_name,
                                                         subject_list[s].acronym)
                        subj_name_hours[subject_list[s].acronym] -= 2
                        s = (s+1)%len(subject_list)

                    # 3rd case: this hour is assined to theory but there's only one hour left to assign with
                    # actual subject in s.
                    elif self.structure[it,h,d] == 'T' and subj_name_hours[subject_list[s].acronym] == 1 \
                            and self.time_table[it, h, d] == Cell():
                        # filter subjects with just one hour left to assign to make a block of two
                        odd_subjects = list(filter(lambda x: x[1] == 1 and x[0] != subject_list[s].acronym,
                                                   subj_name_hours.items()))

                        # is there's more subjects, we make a block of two
                        if odd_subjects != [] and self.time_table[it, h+1, d] == Cell():
                            self.time_table[it, h+1, d] = Cell(group.name, group.classroom.classroom_name,
                                                               odd_subjects[0][0])
                            subj_name_hours[odd_subjects[0][0]] -= 1

                        self.time_table[it,h,d] = Cell(group.name, group.classroom.classroom_name,
                                                       subject_list[s].acronym)
                        subj_name_hours[subject_list[s].acronym] -= 1
                        s = (s+1)%len(subject_list)
                    # 4rd case: same as 3rd but without block of two
                    elif self.structure[it, h+1, d] == 'T' and subj_name_hours[subject_list[s].acronym] == 1 \
                         and self.time_table[it, h+1, d] == Cell():

                        self.time_table[it, h+1, d] = Cell(group.name, group.classroom.classroom_name,
                                                         subject_list[s].acronym)
                        subj_name_hours[subject_list[s].acronym] -= 1
                        s = (s + 1) % len(subject_list)



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
                        elif th_hours == 1 and lab_hours == 1:
                            if is_lab_hour[hour, day]:
                                self.structure[it, hour, day] = 'T'
                                self.structure[it, hour+1, day] = 'L'
                                is_lab_hour[hour+1, day] = True
                            else:
                                self.structure[it, hour, day] = 'L'
                                self.structure[it, hour+1, day] = 'T'
                                is_lab_hour[hour, day] = 'L'
                            lab_hours -= 1
                            th_hours -= 1
                        elif th_hours == 1:
                            self.structure[it, hour, day] = 'T'
                            th_hours -= 1
                        elif lab_hours == 1:
                            self.structure[it, hour, day] = 'L'
                            is_lab_hour[hour, day] = True
                            lab_hours -= 1
                        else:
                            break
                        else:
                            break

    def compute_best_cells(self, group, subject_list, subjects_index, n_hours):
        easy = True
        indexes = []
        for i in subjects_index:
            if subject_list[i].practical_hours % 2 != 0:
                easy = False
                indexes.append(i)

        if easy:
            cell1 = PracticeCell(group=group.name,
                                subjects=[subject_list[i] for i in subjects_index],
                                classrooms=[])
            for i in subjects_index:
                n_hours[i] -= 2

            return cell1, cell1

        else:
            cell = PracticeCell(group=group.name)
            subjects = []
            for i in subjects_index:
                if subject_list[i].practical_hours % 2 == 0:
                    n_hours[i] -= 2
                    subjects.append(subject_list[i])
                else:
                    subjects.append("EM")
            cell.subjects=subjects

            return cell, cell

    def recalculate_subjects(self, subject_list):
        ind = []
        for i in range(len(subject_list)):
            if subject_list[i].practical_hours == 1 or subject_list[i].practical_hours == 3:
                ind.append(i)
        new_list = []
        for i in range(len(subject_list)):
            if i not in ind:
                new_list.append(subject_list[i])

        # join the subjects in ind


    def assign_lab_hours(self, semester):
        for group, it in zip(self.groups.values(), range(len(self.groups.items()))):
            # get subjects and its practical hours
            subject_list = self.__get_subj_list__(group)
            shuffle(subject_list)

            self.recalculate_subjects(subject_list)

            # compute range of shift
            if group.shift == 'M':
                start_range, end_range = 0, self.time_table.shape[1] // 2
            else:
                start_range, end_range = self.time_table.shape[1] // 2, self.time_table.shape[1]

            subjects_index = [i for i in range(group.numsubgroups)]

            days_week = self.structure.shape[2]

            n_hours = [i.practical_hours * group.numsubgroups for i in subject_list]

            for hour in range(start_range, end_range, 2):
                for day in range(days_week):
                    # if the cell is a lab cell, let's fill it
                    if self.structure[it, hour, day] == 'L':
                        cell1, cell2 = self.compute_best_cells(group, subject_list, subjects_index, n_hours)
                        # cell = PracticeCell(group=group.name,
                        #                     subjects=[subject_list[i] for i in subjects_index],
                        #                     classrooms=[])
                        self.time_table[it, hour, day] = cell1
                        self.time_table[it, hour + 1, day] = cell2

                        subjects_index = list(map(lambda x: (x + 1) % len(subject_list), subjects_index))

