class Cell:
    def __init__(self, group = "empty", classroom = "empty", subject = "empty"):
        self.group = group
        self.classroom = classroom
        self.subject = subject

    def empty(self):
        return self.group == "empty" and self.classroom == "empty" and self.subject == "empty"

    # equality operator overload
    def __eq__(self, other):
        return self.group == other.group and self.classroom == other.classroom and self.subject == other.subject


    def __repr__(self):
        return self.group + " " + self.subject + " " + self.classroom

