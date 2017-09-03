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
    data = pd.read_csv(filepath_or_buffer=file, sep=";", true_values=["T"], false_values=["F"])

    for row in data.iterrows():
        aux = obj_class()
        d = dict(row[1]) # convert data row in dictionary
        for k,v in d.items():
            lk = str.lower(k)
            if lk in dir(aux): # check if data header name is an attribute of actual object
                if not obj_class._meta.get_field(lk).is_relation: 
                    aux.__setattr__(lk, v)
                else: # if it's a relation, search the object in database
                    foreign_class = getattr(import_module(module_name), k)
                    if obj_class._meta.get_field(lk).many_to_one:
                        fk = foreign_class.objects.get(name=v)
                        aux.__setattr__(lk, fk)
                    else: #ManyToMany field
                        aux.save()
                        if row[1].isnull().sum() == 0:
                            classes = str(v).split(',')
                            for c in classes:
                                fk = foreign_class.objects.get(name=c)
                                aux.__getattribute__(lk).add(fk)
        aux.save()
