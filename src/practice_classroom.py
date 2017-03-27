import numpy as np
from classroom import ClassRoom

def create_practice_classroom(filename, days, hours_per_day):
    # Empty list of different classrooms
    classroom = {}
    with open(filename, 'r') as f:
        # Skip the name of the columns
        f.readline()
        # Load data
        for line in f:
            l = line[:-1].split(',')
            materials = l[-1].split('-')
            classroom[l[0]] = PracticeClassRoom(materials, days, hours_per_day, 
                              l[0], int(l[1]))

    return classroom

class PracticeClassRoom (ClassRoom):

    def __init__(self, materials, days, hours_per_day, name, capacity):
        super().__init__(days=days, hours=hours_per_day, name=name, capacity=capacity)
        self.materials = materials

    def __repr__(self):
        return str(self.capacity) + " " + self.classroom_name + " " + str(self.materials)
