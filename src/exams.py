import numpy as np
from subject import Subject
from cell import Cell

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
        self.time_table = np.full((len(subjects), 2, n_days), fill_value=Cell(), dtype=Cell)
        self.groups = groups
        self.classrooms = classrooms
        self.subjects = subjects
        self.semester = semester
        self.years = n_years


    """
                            Order subjects
        
        To create a non frustrating exams period, it's necessary
        to know how difficult a subject is. This it's very subjective,
        but the number of students it's a good indicator of the difficulty
        of the subject. So, this function order the subjects based on the
        number of students.
    """

    def __order_subjects__(self):

        self.ordered_subjects = {1:[], 2:[], 3:[]}

        for subject in self.subjects: