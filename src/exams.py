import numpy as np
from cell import Cell
from operator import itemgetter
# from itertools import takewhile, dropwhile

class Exams:

    """ Class to create a time table for the exams period"""

    """
            Init of the object

         * n_days: how many days do the exams last
         * groups: list with all the groups of the center
         * classrooms: list with all the theoretical classrooms of the center
         * subjects: dict with all the subjects
         * semester: describe if the timetable it's for the first semester or the second
         * years: length in years of the degree

    """

    def __init__(self, n_days, groups, classrooms, subjects, semester, n_years = 4):
        self.time_table = np.full((n_years, 2, n_days), fill_value=Cell(), dtype=Cell)
        self.groups = groups
        self.classrooms = classrooms
        self.subjects = subjects
        self.semester = semester
        self.years = n_years
        self.ordered_subjects = self.__order_subjects__()
        print(self.time_table)

    """
                            Order subjects
        
        To create a non frustrating exams period, it's necessary
        to know how difficult a subject is. This it's very subjective,
        but the number of students it's a good indicator of the difficulty
        of the subject. So, this function order the subjects based on the
        number of students.
    """

    def __order_subjects__(self):
        # sort = sorted(self.subjects.items(), key=itemgetter(1))

        return sorted(self.subjects.items(), key=itemgetter(1))

        # for year in range(self.years):
        #     self.ordered_subjects[year] = list(takewhile(lambda x: x[1].year == year+1, sort))
        #     sort = list(dropwhile(lambda x: x[1].year == year+1, sort))

        # print(self.ordered_subjects)



    def __compute_exams_weights__(self):
        weights = np.array([subject[1].n_students for subject in self.ordered_subjects], dtype=np.float64)

        weights = weights / np.sum(weights)

        for subject, weight in zip(weights, self.ordered_subjects):
            print(subject, weight)

        return weights




