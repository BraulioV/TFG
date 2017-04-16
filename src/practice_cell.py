from cell import Cell
"""
This class represents a lab cell in the time table, where there are
subgroups of the original one. Each with a different subject
"""
class PracticeCell (Cell):
    def __init__(self, group="-", subjects=[], classrooms=[]):
        super().__init__(group=group)
        self.subjects = subjects
        self.classrooms = classrooms

    def __repr__(self):
        return self.group + " " + str(self.subjects) 