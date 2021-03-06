from django.db import models

class Classroom(models.Model):
    name       = models.CharField(max_length=50)
    capacity   = models.PositiveSmallIntegerField(default=0)
    ispractice = models.CharField(max_length=2,default='Yes')

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
