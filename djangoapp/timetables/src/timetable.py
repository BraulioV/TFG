from .cell import Cell
from .practice_cell import PracticeCell
from .subject import Subject
import numpy as np
from random import shuffle, choices
from itertools import takewhile, dropwhile
from copy import deepcopy
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
                subjects, semester, class_dict):
        self.days = n_days
        self.hours = n_hours
        self.time_table = np.full((len(groups), n_hours, n_days), fill_value = Cell(), dtype=Cell)
        self.structure = np.full((len(groups), n_hours, n_days), fill_value='E', dtype=str) # empty
        self.groups = dict(filter(lambda g: semester in g[1].semester, groups.items()))
        self.classrooms = classrooms
        self.practices_classrooms = practices_classrooms
        self.subjects = dict(filter(lambda s: s[1].semester == semester, subjects.items()))
        self.semester = semester
        self.possible_pr_classrooms = {}
        # self.__get_possible_classrooms__()
        self.lab_class_dict = class_dict

    # define default json encoder
    def dict_timetable(self):
        hours = ['08:30 - 09:30', '09:30 - 10:30', '10:30 - 11:30', '11:30 - 12:30', '12:30 - 13:30', '13:30 - 14:30',
         '15:30 - 16:30', '16:30 - 17:30', '17:30 - 18:30', '18:30 - 19:30', '19:30 - 20:30', '20:30 - 21:30', '21:30 - 22:30']
        return {g:{h:[c.dict_cell() for c in r] for h,r in zip(hours, t)} for g,t in zip(self.groups.keys(), self.time_table)}

    def get_timetable_from_json(self, timetable_json):
        it = 0
        for g,timetable_group in timetable_json.items():
            for timetable_week,h in zip(timetable_group.values(), range(self.hours)):
                for timetable_cell,d in zip(timetable_week, range(self.days)):
                    if not timetable_cell['ispractice'] and timetable_cell['subject'] == '-':
                        cell = Cell()
                    else:
                        cell = PracticeCell(subjects=timetable_cell['subject'], classrooms=timetable_cell['classroom']) \
                               if timetable_cell['ispractice'] \
                               else Cell(group=g, subject=timetable_cell['subject'], classroom=timetable_cell['classroom'])

                    self.time_table[it,h,d] = cell
            it+=1

    def __get_subj_list__(self, group):
        return list(filter(lambda x: x.year == group.year and x.speciality == group.speciality,
                           self.subjects.values()))


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

    def __assign_th_cell__(self, it, h, d, group, acronym, subj_name_hours, n_hours=2):
        if n_hours == 2:
            self.time_table[it, h, d] = Cell(group.name, group.classroom.classroom_name, acronym)
            self.time_table[it, h + 1, d] = Cell(group.name, group.classroom.classroom_name, acronym)
            bloque = None
        else:
            # filter subjects with just one hour left to assign to make a block of two
            if any(self.__is_odd__(x[1]) and x[0] != acronym for x in subj_name_hours.items()):
                odd_subjects = list(filter(lambda x: self.__is_odd__(x[1]) and x[0] != acronym, subj_name_hours.items()))
            else:
                odd_subjects = list(filter(lambda x: x[1] > 0 and x[0] != acronym, subj_name_hours.items()))

            # is there's more subjects, we make a block of two
            if odd_subjects != [] and self.time_table[it, h + 1, d] == Cell():
                bloque = odd_subjects[0][0]
                self.time_table[it, h + 1, d] = Cell(group.name, group.classroom.classroom_name, odd_subjects[0][0])
                subj_name_hours[odd_subjects[0][0]] -= 1
            else:
                bloque = None

            self.time_table[it, h, d] = Cell(group.name, group.classroom.classroom_name, acronym)

        subj_name_hours[acronym] -= n_hours
        if subj_name_hours[acronym] == 0:
            return True, bloque
        else:
            return False, bloque

    __is_odd__ = lambda self, x: bool(x&1)

    def __shuffle_priority__(self, my_list):
        shuffle(my_list)
        # we sort the subjects by theory_hours
        my_list.sort(key=lambda s: s.theoretical_hours, reverse=True)

    def random_greedy_theory(self):
        for group, it in zip(self.groups.values(), range(self.time_table.shape[0])):
            # we get the subjects and its, theoretical hours
            subject_list = self.__get_subj_list__(group)

            self.__shuffle_priority__(subject_list)
            subj_name_hours = {subject.acronym:subject.theoretical_hours for subject in subject_list}
            s = 0

            if group.shift == 'M':
                start_range, end_range = 0, self.time_table.shape[1] // 2

            else:
                start_range, end_range = self.time_table.shape[1] // 2, self.time_table.shape[1]


            for h in range(start_range, end_range, 2):
                for d in range(self.time_table.shape[2]):
                    if subject_list == []:
                        break

                    # 1st case: this hour is assigned to lab/is empty
                    elif (self.structure[it,h,d] == 'L' or self.structure[it,h,d] == 'E') \
                            and self.structure[it, h+1, d] != 'T':
                        remove = False
                        asignado = False

                    # 2nd case: this hour is assigned to theory and we can make a 2 hours block with actual
                    # subject in s.
                    elif self.structure[it,h,d] == 'T' and subj_name_hours[subject_list[s].acronym] >= 2\
                            and self.time_table[it,h,d] == Cell() and self.time_table[it,h+1,d] == Cell():
                        remove, block = self.__assign_th_cell__(it, h, d, group, subject_list[s].acronym, subj_name_hours)
                        asignado = True

                    # 3rd case: this hour is assined to theory but there's only one hour left to assign with
                    # actual subject in s.
                    elif self.structure[it,h,d] == 'T' and subj_name_hours[subject_list[s].acronym] == 1 \
                            and self.time_table[it, h, d] == Cell():
                        remove, block = self.__assign_th_cell__(it, h, d, group, subject_list[s].acronym, subj_name_hours, 1)
                        asignado = True

                    # 4rd case: same as 3rd but without block of two
                    elif self.structure[it, h+1, d] == 'T' and subj_name_hours[subject_list[s].acronym] == 1 \
                         and self.time_table[it, h+1, d] == Cell():
                        remove, block = self.__assign_th_cell__(it, h+1, d, group, subject_list[s].acronym, subj_name_hours, 1)
                        asignado = True

                    if remove:
                        del subject_list[s]
                        if block is not None:
                            if subj_name_hours[block] == 0:
                                remove_block = [i for i in subject_list if i.acronym == block]
                                del subject_list[subject_list.index(remove_block[0])]
                        s = (s + 1) % len(subject_list) if s != 0 and subject_list != [] else 0
                    elif asignado:
                        s = (s + 1) % len(subject_list)

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
    def compute_total_hours(self, years):

        hours_year = {}

        # subjects = self.subjects.items()

        for year in years:
            th_ph_hours = [0,0]
            aux = list(filter(lambda x: x.year == year, self.subjects.values()))

            for subject in aux[:5]:
                th_ph_hours[0] += subject.theoretical_hours
                th_ph_hours[1] += subject.practical_hours

            hours_year[year] = tuple(th_ph_hours)

        return hours_year

    def change_structure(self, it, hour, day, kind):
        self.structure[it, hour, day] = kind
        self.structure[it, hour + 1, day] = kind

    def preassignate_hour_by_year(self, shift):
        # filter groups in given shift
        local_groups = dict(filter(lambda x: x[1].shift == shift, self.groups.items()))

        # compute total theory/lab hours for each year
        hours = self.compute_total_hours(set(map(lambda x: x.year, local_groups.values())))
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
            # if lab hours is an odd number, we increase this number by one
            lab = lab+1 if self.__is_odd__(lab) else lab

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
                # if lab hours is an odd number, we increase this number by one
                lab_hours = lab_hours + 1 if self.__is_odd__(lab_hours) else lab
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

    def search_suitable_lab(self, subject, hour, day, two_cells = True):
        # for each of the possible practices classrooms for that subject
        classrooms = list(self.lab_class_dict[subject.acronym])
        shuffle(classrooms)
        for classroom in classrooms:
            if two_cells:
                # if it is free at that time, use that classroom and mark it as occupied
                if not self.practices_classrooms[classroom].time_table[hour, day] and \
                        not self.practices_classrooms[classroom].time_table[hour + 1, day]:
                    self.practices_classrooms[classroom].time_table[hour, day] = True
                    self.practices_classrooms[classroom].time_table[hour + 1, day] = True
                    # return self.practices_classrooms[classroom]
                    lab = self.practices_classrooms[classroom]
                    break
            else:
                if not self.practices_classrooms[classroom].time_table[hour, day]:
                    self.practices_classrooms[classroom].time_table[hour, day] = True
                    lab = self.practices_classrooms[classroom]
                    break
                    # return self.practices_classrooms[classroom]
        else:
            return " "
        return lab




    def compute_best_cells(self, group, subject_list, subjects_index, hours, hour, day):
        # if the subjects doesn't have anymore
        # hours to assign, returns an empty subject
        def subject_or_not(subject, index):
            if hours[index] > 0 and subject != Subject():
                hours[index] -= 1
                return subject
            else:
                return Subject()


        # Generate two new cells
        cell1 = PracticeCell(group=group.name)
        cell2 = PracticeCell(group=group.name)

        subjects_c1, subjects_c2 = [None] * group.numsubgroups, [None] * group.numsubgroups
        lab_c1, lab_c2 = [''] * group.numsubgroups, [''] * group.numsubgroups

        it = 0
        for i in subjects_index:
            # if the "subject" is the union of two,
            # split them and assign them
            if type(subject_list[i]) == tuple:
                subjects_c1[it] = subject_or_not(subject_list[i][0], i)
                subjects_c2[it] = subject_or_not(subject_list[i][1], i)
                if subject_list[i][1] == Subject():
                    lab = self.search_suitable_lab(subject_list[i][0], hour, day, False)
                else:
                    lab = self.search_suitable_lab(subject_list[i][0], hour, day)

                lab_c1[it]= lab
                if subject_list[i][1] != Subject():
                    lab_c2[it] = lab
            # otherwise, just assign the subject
            else:
                subjects_c1[it] = subject_or_not(subject_list[i], i)
                subjects_c2[it] = subject_or_not(subject_list[i], i)
                lab = self.search_suitable_lab(subject_list[i], hour, day)
                lab_c1[it], lab_c2[it] = lab, lab
            it += 1

        cell1.subjects, cell1.classrooms = subjects_c1, lab_c1
        cell2.subjects, cell2.classrooms = subjects_c2, lab_c2


        return cell1, cell2

    def recalculate_subjects(self, subjects, n_groups):
        # search the subjects with odd lab hours
        ind = []
        subject_list = list(filter(lambda x: x.practical_hours > 0, subjects))
        for i in range(len(subject_list)):
            if subject_list[i].practical_hours == 1 or subject_list[i].practical_hours == 3:
                ind.append(i)
        new_list = []
        # and add all the subjects with even lab hours
        for i in range(len(subject_list)):
            if i not in ind:
                new_list.append(subject_list[i])

        # join the subjects in ind
        if len(ind) >= 2:
            while len(ind) > 1:
                new_list.append((subject_list[ind[0]], subject_list[ind[1]]))
                ind.pop(0); ind.pop(0)

        elif len(ind) == 1 and subject_list[ind[0]].practical_hours == 3:
            aux_2_hours, aux_1_hour = deepcopy(subject_list[ind[0]]), deepcopy(subject_list[ind[0]])
            aux_2_hours.practical_hours -= 1
            aux_1_hour.practical_hours = 1

            new_list.append(aux_2_hours)
            new_list.append((aux_1_hour, Subject()))

        elif len(ind) == 1 and subject_list[ind[0]].practical_hours == 1:
            new_list.append((subject_list[ind[0]], Subject()))

        return new_list

    def assign_lab_hours(self):
        for group, it in zip(self.groups.values(), range(len(self.groups.items()))):
            # get subjects and its practical hours
            subject_list = self.__get_subj_list__(group)
            shuffle(subject_list)

            subject_list = self.recalculate_subjects(subject_list, group.numsubgroups)

            # compute range of shift
            if group.shift == 'M':
                start_range, end_range = 0, self.time_table.shape[1] // 2
            else:
                start_range, end_range = self.time_table.shape[1] // 2, self.time_table.shape[1]

            # compute the index
            subjects_index = [i for i in range(group.numsubgroups)]

            days_week = self.structure.shape[2]
            # compute the total lab hours, for each subject
            hours = list(map(lambda x: x*group.numsubgroups, [subject.practical_hours if type(subject) is not tuple
                     else subject[0].practical_hours + subject[1].practical_hours
                     for subject in subject_list]))
            # start loop
            for hour in range(start_range, end_range, 2):
                for day in range(days_week):
                    # if the cell is a lab cell, let's fill it
                    if self.structure[it, hour, day] == 'L' or self.structure[it, hour, day] == 'E':
                        cell1, cell2 = self.compute_best_cells(group, subject_list, subjects_index, hours, hour, day)
                        self.time_table[it, hour, day] = cell1
                        self.time_table[it, hour + 1, day] = cell2

                        subjects_index = list(map(lambda x: (x + 1) % len(subject_list), subjects_index))
                if sum(hours) == 0: break

