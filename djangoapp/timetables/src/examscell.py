from cell import Cell

class ExamsCell(Cell):
    def __init__(self, classrooms = [], subjects = [], weight = 0):
        self.classroom = classrooms
        self.subject = subjects
        self.actual_weight = weight


    def empty(self):
        return self.classroom == [] and self.subject == []


    def __eq__(self, other):
        return self.classroom == other.classroom and self.subject == other.subject


    def __repr__(self):
        result = "| "

        for subj, classr in zip(self.subject, self.classroom):
            result += " " + subj.acronym + " " + classr

        return result +  " |"


    def is_free(self):
        return self.subject == []
