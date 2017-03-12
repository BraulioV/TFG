from classroom import *
from practice_classroom import *
from group import *
from sub_group import *
from subject import *

if __name__ == '__main__':
    classrooms = create_classroom(filename="../Dataset/classrooms.csv", days=5, 
                                  hours_per_day=4)
    print(classrooms)
    groups = create_group(filename="../Dataset/groups.csv", 
                          classroom_list=classrooms)
    print(groups)
    pclassrooms = create_practice_classroom(filename="../Dataset/practiceclassrooms.csv", days=5, hours_per_day=4)
    print(pclassrooms)
    