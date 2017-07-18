## import statements

def create_subject(filename):
    # Empty dict of different subjects
    subjects, n_years, last_year = {}, -1, -1
    with open(filename, 'r') as f:
        # Skip column names
        f.readline()
        # load data
        for line in f:
            l = line[:-1].split(',')
            materials = set(l[3].split('-'))
            subjects[l[5]] = Subject(name=l[0],
                                     n_th = int(l[1]),
                                     n_ph = int(l[2]),
                                     requirements=set(map(lambda x: str.upper(x), materials)),
                                     split=l[4] == 'True',
                                     acronym=l[5],
                                     speciality=l[6],
                                     year = int(l[7]),
                                     semester = int(l[8]),
                                     degree = l[9],
                                     students = int(l[10]))
            if l[7] != last_year:
                last_year = l[7]
                n_years += 1

    return subjects, n_years

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

    def __init__(self, name="", acronym="", n_th=0, n_ph=0, year=0, semester=0, degree=0, speciality="",
                 requirements = {}, split = False, students=0):

        self.name = name
        self.acronym = acronym
        self.theoretical_hours = n_th
        self.practical_hours = n_ph
        self.year = year
        self.semester = semester
        self.special_requirements = requirements
        self.split_th_hours = split
        self.degree = degree
        self.speciality = speciality
        self.n_students = students


    # def __repr__(self):
    #     return "Name: " + self.name + "\tAcronym: " + self.acronym + "\tDegree: " \
    #            + self.degree + "\n\t* Theoretical hours: " + \
    #            str(self.theoretical_hours) + "\tPractical hours: " + \
    #            str(self.practical_hours) + "\n\tYear: " + str(self.year) + \
    #            "\tSemester: " + str(self.semester) + "\n\tSpecial requirements: " \
    #            + str(self.special_requirements) + "\nSplit theoretical hours: " \
    #            + str(self.split_th_hours) + "\nSpeciality: " + self.speciality + "\n"
    def __repr__(self):
        return self.acronym

    # equality operator overload
    def __eq__(self, other):
        return self.name == other.name and self.acronym == other.acronym and \
               self.theoretical_hours == other.theoretical_hours and self.practical_hours == other.practical_hours and \
               self.year == other.year and self.semester == other.semester and \
               self.special_requirements == other.special_requirements and self.split_th_hours == other.split_th_hours \
               and self.degree == other.degree and self.speciality == other.speciality

    # override < operator
    def __lt__(self, other):
        return self.practical_hours < other.practical_hours

    # override <= operator
    def __le__(self, other):
        return self.practical_hours <= other.practical_hours

    # override > operator
    def __gt__(self, other):
        return self.practical_hours > other.practical_hours

    # override >= operator
    def __ge__(self, other):
        return self.practical_hours >= other.practical_hours
