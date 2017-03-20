from classroom import *
from group import *
from subject import *
from sub_group import *
from practice_classroom import *
from timetable import *

if __name__ == '__main__':
    classrooms = create_classroom(filename="../Dataset/classrooms.csv", days=5, 
                                  hours_per_day=4)
    print(classrooms)
    groups = create_group(filename="../Dataset/groups.csv", 
                          classroom_list=classrooms)
    print(groups)
    subjects = create_subject(filename="../Dataset/subjects.csv")
    print(subjects)
    pclassrooms = create_practice_classroom(filename="../Dataset/practiceclassrooms.csv", days=5, hours_per_day=4)
    print(pclassrooms)

    # create a timetable object
    timetable = TimeTable(n_days=5, n_hours=8, groups=groups, 
                          classrooms=classrooms, practices_classrooms=pclassrooms,
                          subjects=subjects)
    timetable.random_greedy()
    print(timetable.time_table)