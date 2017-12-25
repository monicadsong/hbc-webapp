import os, sys
#from sets import Set
import flask as fk
from functools import wraps

from g import app

import user_manager as um

def login_required(f):
  """ 
    login_required decorator. All of web access is controlled by this routine
  """
  @wraps(f)
  def wrapper(*args, **kwargs):
    name = fk.request.cookies.get('user_id')
    if not um.is_valid_user(name): 
      return "You need to login first", 401 
    else:
      return f(*args, **kwargs)

  return wrapper

@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def user_login():
  if fk.request.method == 'POST':
    user_name = fk.request.form['username']
    password = fk.request.form['password']
    if um.login(user_name, password):
      resp = fk.make_response(fk.redirect("/index"))
      resp.set_cookie('user_id', fk.request.form['username'])
      return resp 
    else:
      return "Ether username or password is not correct, please try again", 406
  else:
    return fk.render_template('login.html')

@app.route('/logout')
@login_required
def logout():
  # TODO: need to close session
  name = fk.request.cookies.get('user_id')
  return fk.redirect("/login")

"""
Browser index
"""
@app.route('/home')
@app.route('/index')
@login_required
def index():
  return fk.render_template("index.html") 

"""
Database management
"""
@app.route("/manage_database", methods=['GET', 'POST'])
@login_required
def manage_database():
  user_id = fk.request.cookies.get('user_id')
  if fk.request.method == 'POST':
    if "update" in fk.request.form:
      user_data = {}
      user_data["firstname"] = fk.request.form["firstname"]
      user_data["lastname"]  = fk.request.form["lastname"]
      user_data["email"]  = fk.request.form["email"]
      user_data["nonharvard"]  = fk.request.form["nonharvard"]
      user_data["choreographer"]  = fk.request.form["choreographer"]

      print("user_data: ", user_id, user_data)
      um.user_update(user_id, user_data)
      db_list = um.get_user_data_list()
      return fk.render_template('database_manager.html', data_list=db_list, user_name=user_id)
    else:
      raise("This button has not been handled yet")
  elif fk.request.method == 'GET':
    db_list = um.get_user_data_list()
    return fk.render_template('database_manager.html', data_list=db_list, user_name=user_id)



@app.route("/add_users", methods=['GET', 'POST'])
#@login_required
def add_users():
  user_id = fk.request.cookies.get('user_id')
  if fk.request.method == 'POST':
    print (fk.request.form)
    if "update" in fk.request.form:
      print ('update in')
      user_data = {}
      user_data["firstname"] = fk.request.form["firstname"]
      user_data["lastname"]  = fk.request.form["lastname"]
      user_data["email"]  = fk.request.form["email"]
      if 'nonharvard' in fk.request.form:
        user_data['nonharvard'] = True
      else: 
        user_data['nonharvard'] = False
      if 'choreographer' in fk.request.form:
        user_data['choreographer'] = True
      else: 
        user_data['choreographer'] = False

      um.add_user(user_data)
      db_list = um.get_user_data_list()
      return fk.render_template('add_user_v2.html', data_list = db_list)
  elif fk.request.method == 'GET':
    print ('fk get')
    db_list = um.get_user_data_list()
    return fk.render_template('add_user_v2.html', data_list = db_list)



@app.route("/delete_user", methods=['POST'])
#@login_required
def delete_user():
  user = fk.request.form['username']
  um.del_user(user)
  db_list = um.get_user_data_list()
  return fk.render_template('add_user_v2.html', data_list = db_list)

@app.route("/add_pieces", methods=['GET', 'POST'])
#@login_required
def add_pieces():
  if fk.request.method == 'POST':
    #print ('post')
    pieces = {}
    for item in fk.request.form:
      #print (item, fk.request.form[item])
      [choreographer, dancer] = item.split(',')
      #print (item.split(','))
      if choreographer in pieces:
        pieces[choreographer] = pieces[choreographer] + ', ' + dancer
      else:
        pieces[choreographer] = dancer
    
    print ('pieces', pieces)
    um.add_pieces(pieces)
  db_list = um.get_user_data_list()
  choreographer_list = um.get_choreographers(db_list)
  return fk.render_template('add_pieces.html', choreographer_list = choreographer_list, dancer_list = db_list)


@app.route("/define_times", methods=['GET', 'POST'])
#@login_required
def define_times():
  if fk.request.method == 'POST':
    time_data = {}
    time_data['start_date'] = fk.request.form['start_date']
    time_data['end_date'] = fk.request.form['end_date']
    time_data['start_time'] = fk.request.form['start_time']
    time_data['end_time'] = fk.request.form['end_time']
    print (time_data, 'time data views')
    um.change_time(time_data)

  return fk.render_template('times.html', current_time = um.get_time())

@app.route("/add_availability", methods=['GET', 'POST'])
#@login_required
def add_availability():
  user_id = fk.request.cookies.get('user_id')
  print (user_id, 'user_id')
  if fk.request.method == 'POST':
    #print ('post')
    availability = ''
    for item in fk.request.form:
      availability = availability + item + ';'
    um.user_update(user_id, availability)
  time_data = um.get_time()
  days = um.create_dates(time_data)
  hours = um.get_hours(time_data)
  avail = um.get_availability(user_id)
  return fk.render_template('availability.html', days = days, hours = hours, avail = avail, user_name = user_id)

@app.route("/create_schedule", methods=['GET'])
#@login_required
def create_schedule():
  db_list = um.get_user_data_list()
  choreographer_list = um.get_choreographers(db_list)
  return fk.render_template('run_solver.html', choreographer_list = choreographer_list, data_list = db_list)









