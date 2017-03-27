from classroom import *
from group import *
from subject import *
from sub_group import *
from practice_classroom import *
from timetable import *

HOURS = 8
DAYS = 5

if __name__ == '__main__':
    classrooms = create_classroom(filename="../Dataset/classrooms.csv", days=DAYS,
                                  hours_per_day=HOURS)
    # print(classrooms)
    groups = create_group(filename="../Dataset/groups.csv", 
                          classroom_list=classrooms)
    # print(groups)
    subjects = create_subject(filename="../Dataset/subjects.csv")
    subjects1 = dict(filter(lambda s: s[1].semester == 1, subjects.items()))
    # print(subjects)
    pclassrooms = create_practice_classroom(filename="../Dataset/practiceclassrooms.csv", days=DAYS, hours_per_day=HOURS)
    # print(pclassrooms)

    # create a timetable object
    timetable = TimeTable(n_days=DAYS, n_hours=HOURS, groups=groups,
                          classrooms=classrooms, practices_classrooms=pclassrooms,
                          subjects=subjects1, semester=1)
    timetable.random_greedy(1)
    print(timetable.time_table)