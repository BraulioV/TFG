class Cell:
    def __init__(self, group = "-", classroom = "-", subject = "-"):
        self.group = group
        self.classroom = classroom
        self.subject = subject

    def empty(self):
        return self.group == "-" and self.classroom == "-" and self.subject == "-"

    # equality operator overload
    def __eq__(self, other):
        return self.group == other.group and self.classroom == other.classroom and self.subject == other.subject


    def __repr__(self):
        if self.empty():
            return ""
        else:
            return self.subject + " " + self.classroom


    def is_free(self, window=None, subj_name_hours=None):
        return self.subject == '-'