from classroom import *
from group import *
from subject import *
from sub_group import *
from practice_classroom import *
from timetable import *
from exams import *
# pretty print
from tabulate import tabulate

HOURS = 12
DAYS = 5

if __name__ == '__main__':
    classrooms = create_classroom(filename="../Dataset/classrooms.csv", days=DAYS,
                                  hours_per_day=HOURS)
    # print(classrooms)
    groups = create_group(filename="../Dataset/groups.csv", 
                          classroom_list=classrooms)

    # filter groups of 1st semester
    groups1 = dict(filter(lambda g: '1' in g[1].semester, groups.items()))

    # print(groups)
    subjects, n_years = create_subject(filename="../Dataset/subjects.csv")
    pclassrooms = create_practice_classroom(filename="../Dataset/practiceclassrooms.csv",
                                            days=DAYS, hours_per_day = HOURS)

    # filter subjects of 1st semester
    subjects1 = dict(filter(lambda s: s[1].semester == 1, subjects.items()))

    # create a timetable object
    timetable = TimeTable(n_days=DAYS, n_hours=HOURS, groups=groups1,
                          classrooms=classrooms, practices_classrooms=pclassrooms,
                          subjects=subjects1, semester=1)

    timetable.__get_possible_classrooms__()
    timetable.preassignate_hour_by_year(shift='M')
    timetable.preassignate_hour_by_year(shift='T')

    # exams = Exams(n_days = 10, groups = groups, classrooms = classrooms,
    #               subjects = subjects, semester = 1, n_years = n_years)

    # timetable.asign_hours(1)
    for table, group in zip(timetable.structure, groups1):
        print(group)
        print(tabulate(table, tablefmt="grid"))
    # exams.__compute_exams_weights__()

    # timetable.random_greedy_theory(1)
    #timetable.random_greedy_practice(1)
    # print(timetable.time_table)