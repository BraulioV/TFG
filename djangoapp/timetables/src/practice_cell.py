from .cell import Cell
from .subject import Subject
from .practice_classroom import PracticeClassRoom

"""
This class represents a lab cell in the time table, where there are
subgroups of the original one. Each with a different subject
"""
class PracticeCell (Cell):
    def __init__(self, group="-", subjects=[], classrooms=[]):
        super().__init__(group=group)
        self.subjects = subjects
        self.classrooms = classrooms

    def empty(self):
        return self.subjects == [] and self.classrooms == []

    def is_free(self, window, subj_name_hours):
        # comprobamos si la celda está vacía
        if self.subjects == []:
            return True
        # si no está vacía, comprobamos si hay algún hueco
        elif any(map(lambda  x: x.acronym == '', self.subjects)):
            # sacamos los índices del hueco
            indices = {i for i, x in enumerate(self.subjects) if x == Subject()}
            # y sacamos las asignaturas que tienen horas por asignar
            subj = [w.acronym for w in window if sum(subj_name_hours[w.acronym])]
            # y dónde tienen sus huecos
            indices_huecos = {i for s in subj for i,x in enumerate(subj_name_hours[s]) if x==1}
            return indices.intersection(indices_huecos) != set()
        else:
            return False

    def __repr__(self):
        return str(self.subjects) + " " + str(self.classrooms)

    def dict_cell(self):
        return {'classroom': [c.classroom_name if isinstance(c,PracticeClassRoom) else c for c in self.classrooms], 
                'subject': [s.acronym for s in self.subjects], 'ispractice': True}
