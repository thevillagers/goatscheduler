from goatscheduler.Task import Task 
from goatscheduler.Schedule import Schedule 
import gc 




def return_1():
    return 1

def return_2():
    return 2 



scrape_zillow   = Task(name='scrape_zillow', callable=return_1)
scrape_redfin   = Task(name='scrape_refin', callable=return_1)
scrape_mls      = Task(name='scrape_mls', callable=return_1)

load_new_files  = Task(name='load_new_files', callable=return_1)
process_new_files = Task(name='process_new_files', callable=return_1)

[scrape_zillow, scrape_redfin, scrape_mls] >> load_new_files

load_new_files >> process_new_files

scraping_schedule           = Schedule(name='scraping_schedule', components=[scrape_zillow, scrape_redfin, scrape_mls])
file_processing_schedule = Schedule(name='file_processing_schedule', components=[load_new_files, process_new_files])


build_apprec_model = Task(name='build_apprec_model', callable=return_1)
build_rent_model = Task(name='build_rent_model', callable=return_2)
build_website_tables = Task(name='build_website_tables', callable=return_2)


analytics_schedule = Schedule(name='analytics_schedule', components=[build_apprec_model, build_rent_model, build_website_tables])


file_processing_schedule >> analytics_schedule






tasks = []
schedules = []

for obj in gc.get_objects():
    if isinstance(obj, Task):
        tasks.append(obj)
    elif isinstance(obj, Schedule):
        schedules.append(obj)


for task in tasks:
    for schedule in schedules:
        if task in schedule.components:
            print(f'{task.name} is part of schedule {schedule.name}')


print('\n\n\n')
print(scraping_schedule)
print(file_processing_schedule)
print(analytics_schedule)