from cell import Cell
from subject import Subject
"""
This class represents a lab cell in the time table, where there are
subgroups of the original one. Each with a different subject
"""
class PracticeCell (Cell):
    def __init__(self, group="-", subjects=[], classrooms=[]):
        super().__init__(group=group)
        self.subjects = subjects
        self.classrooms = classrooms


    def is_free(self, window):
        # comprobamos si la celda está vacía
        if self.subjects == []:
            return True
        # si no está vacía, comprobamos si hay algún hueco
        elif any(map(lambda  x: x.acronym == '', self.subjects)):
            # si hay algún hueco, comprobamos que coincide con el hueco de la ventana
            if self.subjects.index(Subject()) == window.index(Subject()):
                return True
            else:
                return False
        else:
            return False

    def __repr__(self):
        return self.group + " " + str(self.subjects) 