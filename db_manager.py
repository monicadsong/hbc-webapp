from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import example_users
import helper_db

import sys, os


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

def change_domain(time_string):
  s = _session()
  DOMAIN = s.query(_Domain).first()
  if DOMAIN: 
    DOMAIN.domain = time_string[:-1]
  else: 
    DOMAIN = _Domain(domain = time_string[:-1])
  s.add(DOMAIN)
  s.commit()
  return True

def get_domain():
  s = _session()
  DOMAIN = s.query(_Domain).first()
  if DOMAIN: 
    return DOMAIN.domain
  else: 
    return None

def add_user(user_data={}):
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
      avail = {}
      for a in a_split:
        [date, time] = a.split(',')
        if date in avail:
          avail[date] = avail[date] + ', ' + time + 'pm'
        else:
          avail[date] = time + 'pm'
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

def _search_user(username):
  s = _session()
  try: 
    user = s.query(_Dancer).filter_by(username=username).one()
  except:
    return False 
  else:
    return user

def get_castlist(choreographers):
  castlist = {}
  for x in choreographers:
    performers = []
    for p in x.dancers.split(', '):
        performers.append(_search_user(p))
    castlist[(x.firstname, x.lastname)] = performers
  return castlist

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
    if u.username != 'harvardballetcompany@gmail.com':
      db_list.append(Dummy(u.username, u.firstname, u.lastname, u.nonharvard, u.choreographer, u.dancers, u.availability))
  return sorted(db_list, key = lambda x: x.firstname)


