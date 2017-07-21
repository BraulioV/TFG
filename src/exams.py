import numpy as np
from examscell import ExamsCell
from operator import itemgetter
from itertools import takewhile, dropwhile

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
        self.time_table = np.full((2, n_days), fill_value=ExamsCell(), dtype=ExamsCell)
        self.groups = groups
        self.classrooms = classrooms
        self.subjects = subjects
        self.semester = semester
        self.years = n_years
        self.ordered_by_year = {}
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

        global_order = sorted(self.subjects.items(), key=itemgetter(1))
        sort = list(global_order)


        for year in range(self.years):
            self.ordered_by_year[year] = list(takewhile(lambda x: x[1].year == year+1, sort))
            sort = list(dropwhile(lambda x: x[1].year == year+1, sort))


        return global_order



    def __compute_exams_weights__(self):
        weights = np.array([subject[1].n_students for subject in self.ordered_subjects], dtype=np.float64)

        return weights


    def compute_timetable(self):

        weights = self.__compute_exams_weights__()[::-1]
        total_exams_per_day = np.zeros(2, self.time_table.shape[2])


