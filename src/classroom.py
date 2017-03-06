import numpy as np


class ClassRoom:

    """" Class to model a classroom for a specific bachelor"""

    def __init__(self, d, x, capacity, name):
        self.time_table = np.full((d, x), fill_value=False, dtype=np.bool)
        self.capacity = capacity
        self.classroom_name = name
