from goatscheduler.Task import Task 
from goatscheduler.Schedule import Schedule 






def return_1():
    return 1

def return_2():
    return 2 



mytask = Task(name='mytask', callable=return_1)
mytask2 = Task(name='mytask2', callable=return_2)
mytask3 = Task(name='mytask3', callable=return_2)
mytask4 = Task(name='mytask4', callable=return_1)


mytask >> mytask2 
mytask2 >> mytask4 
mytask3 >> mytask4 

print(mytask)
print(mytask2)
print(mytask3)
print(mytask4)