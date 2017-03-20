import numpy as np


def create_classroom(filename, days, hours_per_day):
    # Empty list of different classrooms
    classroom = {}
    with open(filename, 'r') as f:
        # Skip the name of the columns
        f.readline()
        # Load data
        for line in f:
            l = line[:-1].split(',')
            classroom[l[0]] = ClassRoom(days, hours_per_day, l[0], int(l[1]))

    return classroom


class ClassRoom:

    """ Class to model a classroom for a specific bachelor """

    def __init__(self, d, x, name, capacity):
        self.time_table = np.full((d, x), fill_value=("Empty, Empty"))
        self.capacity = capacity
        self.classroom_name = name

    def __repr__(self):
        return str(self.capacity) + " " + self.classroom_name

    """ Fill a specific hour a classroom """

    def assign_class(self, x, y, group, subject):
        # If time_table[x,y] is empty, assign the
        # group and the subject
        if not self.time_table[x,y]:
            self.time_table[x,y] = [group, subject]
            return True

        return False

    def delete_at(self, x, y):
        self.time_table[x, y] = False
