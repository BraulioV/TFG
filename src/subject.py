## import statements

def create_subject(filename):
    # Empty dict of different subjects
    subjects = {}
    with open(filename, 'r') as f:
        # Skip column names
        f.readline()
        # load data
        for line in f:
            l = line[:-1].split(',')
            materials = l[3].split('-')
            subjects[l[5]] = Subject(name=l[0], acronym=l[5], n_th=int(l[1]),
                                    n_ph=int(l[2]), year=int(l[-3]), degree=l[-1],
                                    semester=int(l[-2]), requirements=materials,
                                    split=l[4]=='True', speciality=l[6])
    return subjects

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
    def __init__(self, name="", acronym="", n_th=0, n_ph=0, year=0, semester=0, degree="", speciality="",
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
        self.speciality = speciality


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