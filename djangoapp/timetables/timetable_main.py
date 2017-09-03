from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")
import django
django.setup()

from .src import classroom, practice_classroom, group, subject, timetable, cell, practice_cell
from timetables.models import *
import sys

def compute_timetable(days, hours):
    """
    function that prepares the data structures that the timetable class needs to work
    """
    classrooms = classroom.create_classroom_from_db(5,10)
    pclassrooms = practice_classroom.create_classroom_from_db(5,10)
    groups = group.create_group_from_db(classrooms)
    subjects, dict_lab_class = subject.create_subject_from_db()
    time_table = timetable.TimeTable(n_days=int(days), n_hours=int(hours), groups=groups,
                          classrooms=classrooms, practices_classrooms=pclassrooms,
                          subjects=subjects, semester=1, class_dict=dict_lab_class)
    # time_table.__get_possible_classrooms__()
    time_table.preassignate_hour_by_year(shift='M')
    time_table.preassignate_hour_by_year(shift='T')
    time_table.random_greedy_theory()
    time_table.assign_lab_hours()

    return time_table
