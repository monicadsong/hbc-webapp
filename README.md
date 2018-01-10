# HBC Tech Week Scheduler
Web application to allow HBC producers to easily create tech week schedules. Built using Flask, SQLALchemy, Jinja, Bootstrap and Python3. 

## Flask Web App
Application runs on an Amazon EC2 instance and is accessible at http://34.207.173.18:5001
Algorithm development available at https://github.com/monicadsong/CS182-Final-Project


### How to Use (Admin): 
1. Add dancers and choreographers
2. Define cast list
3. Set Times
4. Collect dancer availabilities
3. Confirm information, set available stage hours, and run scheduler


### Description of files:
* *g.py, config.py*: configuration files
* *main.py*: launches Flask app
* *classes.py, scheduler.py, solver.py, Tree.py, helper.py*: run the CSP scheduler
* *db_manager.py*: manages dancer and rehearsal information using object-relational mapping with SQLAlchemy
* *helper_db.py*: helper functions for database manager
* *views.py*: view functions to connect database with HTML templates
* *db_manager_tests.py*: test the database manager
* *example_user.py*: example cases
* *templates*: contains the HTML templates
* *static*: contains custom and Bootstrap CSS and Javascript files as well as images

### To Do:
* Add error messages/ alerts
* Allow admin to send emails to dancers
* Allow admin to save scheduler output
* **Connect to domain name**