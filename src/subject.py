## import statements

class Subject:

    """ Class to model a subject """

    """
        Init of the object

     * name: name of the subject
     * acronym: acronym of the subject
     * n_th: number of theoretical hours
     * n_ph: number of practical hours
     * year: when is the subject taught
     * semester: the subject belongs to the first semester or second
     * requirements: special requirements of the subject like computers,
                     electrical material, etc. By default, empty.
     * split: if the teacher wants, theoretical hours will
             be taught on separate days. By default, false.
    """
    def __init__(self, name, acronym, n_th, n_ph, year, semester, name
                 requirements = [], split = False):

        self.name = name
        self.acronym = acronym
        self.theoretical_hours = n_th
        self.practical_hours = n_ph
        self.year = year
        self.semester = semester
        self.special_requirements = requirements
        self.split_th_hours = split
        self.degree = degree


    def __str__(self):
        return "Name: " + self.name + "\tAcronym: " + self.acronym + "\tDegree: " + self.degree + "\n\t* Theoretical hours: " + \
               self.theoretical_hours + "\tPractical hours: " + self.practical_hours + \
               "\n\tYear: " + self.year + "\tSemester: " + self.semester + "\n\tSpecial requirements: " \
               + self.special_requirements + "\nSplit theoretical hours: " + self.split_th_hours 
