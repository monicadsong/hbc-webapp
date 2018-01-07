from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import example_users

import sys, os
import datetime


_Base = declarative_base()
class _Dancer(_Base):
  __tablename__ = 'dancers'
  id = Column(Integer, primary_key=True)
  username = Column(String)
  firstname = Column(String)
  lastname = Column(String)
  availability = Column(String)
  password = Column(String)
  nonharvard = Column(Boolean)
  choreographer = Column(Boolean)
  dancers = Column(String)


class _Times(_Base):
  __tablename__ = 'times'
  id = Column(Integer, primary_key=True)
  start_date = Column(String)
  end_date = Column(String)
  start_time = Column(Integer)
  end_time = Column(Integer)

class _Domain(_Base):
  __tablename__ = 'domain'
  id = Column(Integer, primary_key=True)
  domain = Column(String)

_engine = create_engine('sqlite:///users.db', echo=False)
_session = sessionmaker()
_session.configure(bind=_engine)
_Base.metadata.create_all(_engine)

def change_time(time_data):
  print (time_data, 'time_data in um')
  s = _session()
  TIME = s.query(_Times).first()
  if TIME: 
    TIME.start_date = time_data['start_date']
    TIME.end_date = time_data['end_date']
    TIME.start_time = time_data['start_time']
    TIME.end_time = time_data['end_time']
  else: 
    TIME = _Times(start_date = time_data['start_date'], end_date = time_data['end_date'] , 
      start_time = time_data['start_time'], end_time = time_data['end_time'])  
  s.add(TIME)
  s.commit()
  return True

def get_time():
  s = _session()
  TIME = s.query(_Times).first()
  if TIME: 
    return TIME
  else: 
    return None

def convert_date(data):
  date1 = data.split('-')
  return [int(x) for x in date1]

def create_dates(time_data):
  d1 = convert_date(time_data.start_date)
  d2 = convert_date(time_data.end_date)
  day2 = datetime.date(d2[0],d2[1],d2[2])
  day1 = datetime.date(d1[0],d1[1],d1[2]) 
  delta = day2 - day1
  dd = []
  for i in range(delta.days + 1):
      dd.append(day1 + datetime.timedelta(days=i))
  days = []
  day_week = {0: "Monday", 1: 'Tuesday', 2:' Wednesday', 3: 'Thursday', 4:'Friday', 5:"Saturday", 6:'Sunday'}
  for d in dd:
      wd = d.weekday()
      days.append((day_week[wd], d))
  return days

def get_hours(time_data):
  return list(range(time_data.start_time, time_data.end_time + 1))

def change_domain(time_string):
  s = _session()
  DOMAIN = s.query(_Domain).first()
  print ('first')
  if DOMAIN: 
    DOMAIN.domain = time_string
  else: 
    DOMAIN = _Domain(domain = time_string)
  s.add(DOMAIN)
  s.commit()
  return True

def get_domain():
  s = _session()
  DOMAIN = s.query(_Domain).first()

  if DOMAIN: 
    return DOMAIN.domain[:-1]
  else: 
    return None

def add_user(user_data={}):
  """
  user_data: dictionary
  """
  s = _session()
  try: 
    s.query(_Dancer).filter_by(username=user_data['email']).one()
  except:
    user = _Dancer(username=user_data['email'], firstname = user_data['firstname'], lastname = user_data['lastname'],
     password= user_data['firstname'] + user_data['lastname'], nonharvard=user_data['nonharvard'], 
     choreographer=user_data['choreographer'], availability = None , dancers = None)
    s.add(user)
    s.commit()

    return True
  else:
    print("User: {} is in database".format(user_data['email']))
    return False


def get_availability(username):
  s = _session()
  q = s.query(_Dancer)
  try: 
    it = s.query(_Dancer).filter_by(username = username).one()
  except:
    print("User: {} is not in database".format(username))
    return False
  else:
    if it.availability:
      a_split = it.availability.split(';')
      print (a_split)
      avail = {}
      for a in a_split:
        [date, time] = a.split(',')
        if date in avail:
          avail[date].append(time)
        else:
          avail[date] = [time]
      return avail
    else:
      return ''


def del_user(username): 
  s = _session()
  q = s.query(_Dancer)
  try: 
    it = s.query(_Dancer).filter_by(username = username).one()
  except:
    print("User: {} is not in database".format(username))
    return False
  else:
    print ('found')
    s.delete(it)
    s.commit()
    print ('deleted')
    return True

def add_pieces(pieces):
  s = _session()
  for p in pieces:
    choreographer = s.query(_Dancer).filter_by(username=p).one()
    choreographer.dancers = pieces[p]
  s.commit()
  return True

#make sure usernames are all lowercase
def user_update(username, availability):
  s = _session()
  try: 
    user = s.query(_Dancer).filter_by(username=username).one()
  except:
    print("no user: ", username)
    return False 
  else:
    print ('added')
    user.availability = availability[:-1]
    s.commit()
    return True

def _print_user_info(u):
  #print("username: ", u.username)
  print("firstname: ", u.firstname)
  print("lastname: ", u.lastname)
  print("username: ", u.username)
  print("password: ", u.password)
  print("nonharvard: ", u.nonharvard)
  print ("choreographer:", u.choreographer)
  print ("availability:", u.availability)
  print("--------------------------------------------")

def show_users():
  s = _session()
  print("All User info") 
  q = s.query(_Dancer)
  for u in q:
    _print_user_info(u)

def login(username, password):
  s = _session()
  try: 
    user = s.query(_Dancer).filter_by(username=username).one()
  except:
    print("no user: ", username)
    return False 
  else:
    if user.password == password:
      return True
    else:
      print("Wrong password")
      return False 

def is_valid_user(username):
  s = _session()
  try: 
    user = s.query(_Dancer).filter_by(username=username).one()
  except:
    return False 
  else:
    return True

def search_user(username):
  s = _session()
  try: 
    user = s.query(_Dancer).filter_by(username=username).one()
  except:
    return False 
  else:
    return user

def get_user_data_list():
  class Dummy:
    def __init__(self, username, firstname, lastname, nonharvard, choreographer, dancers, availability):
      self.username = username
      self.firstname = firstname    
      self.lastname = lastname
      self.nonharvard = nonharvard
      self.choreographer = choreographer  
      self.dancers = dancers
      self.availability = availability

  s = _session()
  q = s.query(_Dancer)

  db_list = []
  for u in q:
    db_list.append(Dummy(u.username, u.firstname, u.lastname, u.nonharvard, u.choreographer, u.dancers, u.availability))
  return db_list


def get_choreographers(db_list):
  return [x for x in db_list if x.choreographer]
if __name__ == '__main__':  
  def test_add_users():
    '''
    user_data_Anna =  {'firstname': 'Anna', 'lastname': 'Antongiorgi', 'availability': '00111100',
                      'nonharvard': False, 'choreographer': True}
    user_data_Emily =  {'firstname': 'Emily', 'lastname': 'Hogan', 'availability': '11111100','nonharvard': True, 'choreographer': False}
    user_data_Angela =  {'firstname': 'Angela', 'lastname': 'Ma','availability': '01111000', 'nonharvard': False, 'choreographer': False}
    '''
    user_data_Anna =  {'email': 'anna@college', 'firstname': 'Anna', 'lastname': 'Antongiorgi', 'nonharvard': False, 'choreographer': True}
    user_data_Emily =  {'email': 'emily@college', 'firstname': 'Emily', 'lastname': 'Hogan', 'nonharvard': True, 'choreographer': False}
    user_data_Angela =  {'email': 'angela@college', 'firstname': 'Angela', 'lastname': 'Ma', 'nonharvard': False, 'choreographer': False}
    add_user(user_data_Anna)
    add_user(user_data_Emily)
    add_user(user_data_Angela)
    print("added users")
    show_users()

  def test_add_example():
    user_data = []
    for dancer in example_users.users:
      print ('dancer',dancer)
      user_dict = {}
      user_dict['firstname'] = dancer[0]
      user_dict['lastname'] = dancer[1]
      user_dict['email'] = dancer[2]
      user_dict['password'] = dancer[3]
      user_dict['nonharvard'] = dancer[4]
      user_dict['choreographer'] = dancer[5]
      user_dict['availability'] = dancer[6]
      user_data.append(user_dict)

    for item in user_data:
      print ('item', item)
      add_user(item)
  def test_update_example():
    for item in example_users.update:
      user_update(item[0], item[1])


  def test_add_pieces():
    pieces = {'anna@college': 'angela@college, mara@college, deedee@college, isabel@college, sarah@wellesley', 
    'mara@college': 'emily@college, arlesia@college', 
    'ali@college': 'anna@college, emily@college, sarah@wellesley, annabel@college'}
    add_pieces(pieces)
    print("added pieces")
    show_pieces()


  def test_del_users():
    del_user('angela@college')  
    print("after deleting user")
    show_users()

  def test_update_users():
    user_data_Anna =  {'availability': '00111100'}
    user_data_Emily =  {'availability': '11111100'}
    user_data_Angela =  {'availability': '01111000'}

    user_update("anna@college", user_data_Anna)
    print("after update data")
    show_users()

  def add_admin():
    admin =  {'email': 'ADMIN', 'firstname': 'password', 'lastname': '', 'nonharvard': False, 'choreographer': False}
    add_user(admin)
    show_users()

  def test_domain():
    print (get_domain())
  #test_update_example()
  test_domain()
  #test_add_example()
  #add_admin()
  #test_update_users()
  #clear_table()
  #test_add_users()
  #user_update('anna@college', '2017-10-16,4;2017-10-16,5;2017-10-16,6;2017-10-16,7;2017-10-16,8;2017-10-16,9;2017-10-16,10;2017-10-16,11;2017-10-17,11;2017-10-18,11;2017-10-19,11;2017-10-20,11;')
  #show_users()
  #test_add_pieces()
  #get_availability('anna@college')
