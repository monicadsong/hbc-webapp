# HBC Tech Week Scheduler

## Flask Web App

### How to Use: 
1. Add Dancers and Choreographers: email address, first name, last name
2. Define Cast list
3. Define Times: define times that you were interested in getting dancer's availabilities
4. Send out emails
3. Confirm information, set available stage times, and run scheduler


#### Description of the files:
* *solver.py*: runs the scheduler
* *scheduler.py*: contains the code for the scheduler class and the three algorithms
* *eval_solution.py*: evaluates a pre-existing actual tech week
* *classes.py*: contains the Dancer and Rehearsal classes
* *helper.py*: contains helper functions referenced by the Scheduler class
* *timeslot_vars.py*: contains the variable values for the time slots
* *Tree.py*: contains helper code for building the search tree
* *InPassage.py, CityScapes.py, Oz.py*: contain the dancer and piece objects for each performance
