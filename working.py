from goatscheduler.Task import Task 
from goatscheduler.Schedule import Schedule 






def return_1():
    return 1

def return_2():
    return 2 



scrape_zillow   = Task(name='scrape_zillow', callable=return_1)
scrape_redfin   = Task(name='scrape_refin', callable=return_1)
scrape_mls      = Task(name='scrape_mls', callable=return_1)


load_new_files  = Task(name='load_new_files', callable=return_1)

[scrape_zillow, scrape_redfin, scrape_mls] >> load_new_files


scrape_schedule = Schedule(name='scrape_schedule', components=[scrape_zillow, scrape_redfin, scrape_mls])

print(scrape_zillow)
print(scrape_redfin)
print(scrape_mls)
print(load_new_files)

print(scrape_schedule)