import numpy as np


def create_classroom(filename, days, hours_per_day):
    # Empty list of different classrooms
    classroom = []
    with open(filename, 'r') as f:
        # Skip the name of the columns
        f.readline()
        # Load data
        for line in f:
            l = line[:-1].split(',')
            classroom.append(ClassRoom(days, hours_per_day, l[0], int(l[1])))

    return classroom


class ClassRoom:

    """" Class to model a classroom for a specific bachelor """

    def __init__(self, d, x, name, capacity):
        self.time_table = np.full((d, x), fill_value=False, dtype=np.bool)
        self.capacity = capacity
        self.classroom_name = name


