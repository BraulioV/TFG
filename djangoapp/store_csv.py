"""
Django script that reads data from a CSV file and stores it on database

USAGE:
python store_csv.py file1.csv Class1 file2.csv Class2...
"""

import pandas as pd
from sys import argv
from itertools import compress, chain, repeat
from importlib import import_module
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE","djangoapp.settings")
import django
django.setup()
from timetables.models import *

def split_in_pairs(split_list):
    """
    Input: ["Element1", "Element2", "Element3", "Element4"]
    Output: (["Element1", "Element3"], ["Element2", "Element4"])
    """
    def compress_elements(split_list, elements, times):
        return compress(split_list, chain.from_iterable(repeat(elements, times)))

    n_times = len(split_list) // 2
    return compress_elements(split_list, [1,0], n_times), compress_elements(split_list, [0,1], n_times)


# separate Class names and file names in two different lists
files, classes = split_in_pairs(argv[1:])
module_name = "timetables.models"

for file, obj_class_name in zip(files, classes):
    # get class
    obj_class = getattr(import_module(module_name), obj_class_name)
    # read data
    data = pd.read_csv(filepath_or_buffer=file)

    for row in data.iterrows():
        aux = obj_class()
        d = dict(row[1])
        for k,v in d.items():
            lk = str.lower(k)
            if lk in dir(aux):
                aux.__setattr__(lk, v)
