from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")
import django
django.setup()

from .src import classroom, practice_classroom, group, subject
from timetables.models import *
# from classroom import *
# from group import *
# from subject import *
# from sub_group import *
# from practice_classroom import *
# from timetable import *
# from exams import *
# from printer import *

def prepare_data(days, hours):
	"""
	function that prepares the data structures that the timetable class needs to work
	"""
	classrooms = classroom.create_classroom_from_db(5,10)
	pclassrooms = practice_classroom.create_classroom_from_db(5,10)
	groups = group.create_group_from_db(classrooms)
	subjects, dict_lab_class = subject.create_subject_from_db()
	print(dict_lab_class)
