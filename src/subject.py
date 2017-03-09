## import statements

class Subject:

    """ Class to model a subject """

    """
        Init of the object

     * name: name of the subject
     * n_th: number of theoretical hours
     * n_ph: number of practical hours
     * requirements: special requirements of the subject like computers,
                     electrical material, etc. By default, empty.
     * split: if the teacher wants, theorical hours will
             be taught on separate days. By default, false.
    """
    def __init__(self, name, n_th, n_ph, requirements = [], split = False):
        self.name = name
        self.theoretical_hours = n_th
        self.practical_hours = n_ph
        self.special_requirements = requirements
        self.split_th_hours = split