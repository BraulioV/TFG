from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")
import django
django.setup()
from timetables.models import *
from classroom import *
from group import *
from subject import *
from sub_group import *
from practice_classroom import *
from timetable import *
from exams import *
from printer import *

def prepare_data():
	"""
	function that prepares the data structures that the timetable class needs to work
	"""


