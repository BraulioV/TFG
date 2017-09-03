from django.db import models

class Classroom(models.Model):
    name       = models.CharField(max_length=50)
    capacity   = models.PositiveSmallIntegerField(default=0)
    ispractice = models.BooleanField(default=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.capacity)

class Subjects(models.Model):
    name       = models.CharField(max_length=200)
    thours     = models.PositiveSmallIntegerField(default=0)
    phours     = models.PositiveSmallIntegerField(default=0)
    acronym    = models.CharField(max_length=10)
    speciality = models.CharField(max_length=200)
    year       = models.PositiveSmallIntegerField(default=0)
    semester   = models.PositiveSmallIntegerField(default=0)
    degree     = models.CharField(max_length=200)
    students   = models.PositiveSmallIntegerField(default=0)
    classroom  = models.ManyToManyField(Classroom)

    def __str__(self):
        return "{}, {}".format(self.name, self.acronym)

class Groups(models.Model):
    name          = models.CharField(max_length=50)
    shift         = models.CharField(max_length=2)
    year          = models.PositiveSmallIntegerField(default=0)
    numsubgroups  = models.PositiveSmallIntegerField(default=0)
    classroom     = models.ForeignKey(Classroom)
    degree        = models.CharField(max_length=200)
    speciality    = models.CharField(max_length=200)
    semester      = models.CharField(max_length=200, 
	                validators=['validate_comma_separated_integer_list'])

    def __str__(self):
        return "{}, {}".format(self.name, self.year)

# class Cell(models.Model):
#     subject   = [models.CharField(max_length=50, default='-')]
#     classroom = [models.CharField(max_length=5, default='-')]

#     def __str__(self):
#         return "{} ({})".format(self.subject.name, self.classroom.name)

# class Timetable(models.Model):
#     group    = models.ForeignKey(Groups)
#     table    = [models.ManyToManyField(Cell)]
#     # row_0830 = models.ManyToManyField(Cell)
#     # row_0930 = models.ManyToManyField(Cell)
#     # row_1030 = models.ManyToManyField(Cell)
#     # row_1130 = models.ManyToManyField(Cell)
#     # row_1230 = models.ManyToManyField(Cell)
#     # row_1330 = models.ManyToManyField(Cell)
#     # row_1530 = models.ManyToManyField(Cell)
#     # row_1630 = models.ManyToManyField(Cell)
#     # row_1730 = models.ManyToManyField(Cell)
#     # row_1830 = models.ManyToManyField(Cell)
#     # row_1930 = models.ManyToManyField(Cell)
#     # row_2030 = models.ManyToManyField(Cell)
