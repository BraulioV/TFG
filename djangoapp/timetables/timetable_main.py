from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")
import django
django.setup()

from .src import classroom, practice_classroom, group, subject, timetable, cell, practice_cell
from .src.printer import generate_pdf
from timetables.models import *
import sys

def compute_timetable(days, hours, semester):
    """
    function that prepares the data structures that the timetable class needs to work
    """
    classrooms = classroom.create_classroom_from_db(days,hours)
    pclassrooms = practice_classroom.create_classroom_from_db(days,hours)
    groups = group.create_group_from_db(classrooms)
    subjects, dict_lab_class = subject.create_subject_from_db()
    time_table = timetable.TimeTable(n_days=int(days), n_hours=int(hours), groups=groups,
                          classrooms=classrooms, practices_classrooms=pclassrooms,
                          subjects=subjects, semester=semester, class_dict=dict_lab_class)
    time_table.preassignate_hour_by_year(shift='M')
    time_table.preassignate_hour_by_year(shift='T')
    time_table.random_greedy_theory()
    time_table.assign_lab_hours()

    return time_table

def make_pdf(timetable_json, days, hours, semester):
    """
    function that prints a pdf with the final timetable
    """
    classrooms = classroom.create_classroom_from_db(days,hours)
    pclassrooms = practice_classroom.create_classroom_from_db(days,hours)
    groups = group.create_group_from_db(classrooms)
    subjects, dict_lab_class = subject.create_subject_from_db()
    time_table = timetable.TimeTable(n_days=int(days), n_hours=int(hours), groups=groups,
                          classrooms=classrooms, practices_classrooms=pclassrooms,
                          subjects=subjects, semester=semester, class_dict=dict_lab_class)
    time_table.get_timetable_from_json(timetable_json)
    generate_pdf(timetable=time_table, name="prueba")
