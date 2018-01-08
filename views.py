import os, sys
import flask as fk
from functools import wraps

from g import app

import db_manager as dm
import helper_db

from solver import solve

def login_required(f):
  """ 
    login_required decorator. All of web access is controlled by this routine
  """
  @wraps(f)
  def wrapper(*args, **kwargs):
    name = fk.request.cookies.get('user_id')
    if not dm.is_valid_user(name): 
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
    if dm.login(user_name, password):
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

@app.route('/admin')
@login_required
def admin():
  user_id = fk.request.cookies.get('user_id')
  if user_id != 'harvardballetcompany@gmail.com': 
    return "Sorry, you don't have access this page.", 403
  else:
    return fk.render_template('admin.html', user_name = user_id)


"""
Browser index
"""
@app.route('/home')
@app.route('/index')
@login_required
def index():
  user_id = fk.request.cookies.get('user_id')
  if user_id == "harvardballetcompany@gmail.com":
    return fk.render_template('admin.html', user_name = user_id)
  else:
    if fk.request.method == 'POST':
      #print ('post')
      availability = ''
      for item in fk.request.form:
        availability = availability + item + ';'
      dm.user_update(user_id, availability)
    time_data = dm.get_time()
    days = helper_db.create_dates(time_data)
    hours = [12,1,2,3,4,5,6,7,8,9,10,11]
    avail = dm.get_availability(user_id)
    return fk.render_template('index.html', days = days, hours = hours, avail = avail, user_name = user_id)


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
      dm.user_update(user_id, user_data)
      db_list = dm.get_user_data_list()
      return fk.render_template('database_manager.html', data_list=db_list, user_name=user_id)
    else:
      raise("This button has not been handled yet")
  elif fk.request.method == 'GET':
    db_list = dm.get_user_data_list()
    return fk.render_template('database_manager.html', data_list=db_list, user_name=user_id)



@app.route("/add_users", methods=['GET', 'POST'])
@login_required
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

      dm.add_user(user_data)
      db_list = dm.get_user_data_list()
      return fk.render_template('add_user.html', data_list = db_list, user_name=user_id)
  elif fk.request.method == 'GET':
    print ('fk get')
    db_list = dm.get_user_data_list()
    return fk.render_template('add_user.html', data_list = db_list, user_name=user_id)



@app.route("/delete_user", methods=['POST'])
#@login_required
def delete_user():
  user_id = fk.request.cookies.get('user_id')
  user = fk.request.form['username']
  dm.del_user(user)
  db_list = dm.get_user_data_list()
  return fk.render_template('add_user.html', data_list = db_list, user_name=user_id)

@app.route("/add_pieces", methods=['GET', 'POST'])
#@login_required
def add_pieces():
  user_id = fk.request.cookies.get('user_id')
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
    dm.add_pieces(pieces)
  db_list = dm.get_user_data_list()
  choreographer_list = helper_db.get_choreographers(db_list)
  return fk.render_template('add_pieces.html', cast_list = dm.get_castlist(choreographer_list), 
    choreographer_list = choreographer_list, dancer_list = db_list, user_name=user_id)


@app.route("/define_times", methods=['GET', 'POST'])
#@login_required
def define_times():
  user_id = fk.request.cookies.get('user_id')
  if fk.request.method == 'POST':
    time_data = {}
    time_data['start_date'] = fk.request.form['start_date']
    time_data['end_date'] = fk.request.form['end_date']
    time_data['start_time'] = 12
    time_data['end_time'] = 11
    print (time_data, 'time data views')
    dm.change_time(time_data)

  return fk.render_template('times.html', current_time = dm.get_time(), user_name=user_id)

@app.route("/add_availability", methods=['POST'])
#@login_required
def add_availability():
  user_id = fk.request.cookies.get('user_id')
  if fk.request.method == 'POST':
    #print ('post')
    availability = ''
    for item in fk.request.form:
      availability = availability + item + ';'
    dm.user_update(user_id, availability)
  time_data = dm.get_time()
  days = helper_db.create_dates(time_data)
  hours = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  avail = dm.get_availability(user_id)
  return fk.render_template('index.html', days = days, hours = hours, avail = avail, user_name = user_id)

@app.route("/stage_time", methods=['GET', 'POST'])
#@login_required

def set_domain():
  user_id = fk.request.cookies.get('user_id')
  def parse_domain(domain):
    dates = {}
    for d in domain.split(';'):
      [date, time] = d.split(',')
      if date in dates:
        dates[date] = dates[date] + ', ' + time + 'pm'
      else:
        dates[date] = time + 'pm'
    return dates

  if fk.request.method == 'GET':
    print ('GET')
    time_data = dm.get_time()
    days = dm.create_dates(time_data)
    hours = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    return fk.render_template('stage_time.html', days = days, hours = hours, user_name = user_id)
  else:
    domain = ''
    for item in fk.request.form:
      domain = domain + item + ';'
    print (domain, 'domain')
    dm.change_domain(domain)
    user_avails = [(x.firstname, x.lastname, dm.get_availability(x.username)) for x in dm.get_user_data_list()]
    return fk.render_template('confirm_info.html', cast_list = dm.get_castlist(helper_db.get_choreographers(get_user_data_list())), 
      data_list = user_avails, domain = parse_domain(dm.get_domain()), user_name = user_id)


@app.route("/confirm", methods=['POST'])
#@login_required
def confirm():
  user_id = fk.request.cookies.get('user_id')
  def parse_slot(slot):
    [date, time] = slot.split(',')
    return date, time
  pieces, violations = solve()
  for p in pieces:
    p.slot = parse_slot(p.slot)
  return fk.render_template('tech_schedule.html', violations = violations, pieces = pieces,
    user_name = user_id)

@app.route("/userguide", methods=['GET'])
#@login_required
def userguide():
  user_id = fk.request.cookies.get('user_id')
  return fk.render_template('userguide.html', user_name = user_id)








