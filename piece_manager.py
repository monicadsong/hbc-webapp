from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import sys, os

_Base = declarative_base()
class _Piece(_Base):
  __tablename__ = 'pieces'
  id = Column(Integer, primary_key=True)
  choreographer = Column(String)
  dancers = Column(String)

_engine = create_engine('sqlite:///pieces.db', echo=False)
_session = sessionmaker()
_session.configure(bind=_engine)
_Base.metadata.create_all(_engine)





def _print_info(u):
  #print("username: ", u.username)
  print("choreographer: ", u.choreographer)
  print ("dancers:", u.dancers)
  print("--------------------------------------------")

def show_pieces():
  s = _session()
  print("All Pieces info") 
  q = s.query(_Piece)
  for u in q:
    _print_info(u)


def get_piece_list():
  class Dummy:
    def __init__(self, choreographer, dancers):
      self.choreographer = choreographer  
      self.dancers
  s = _session()
  q = s.query(_Piece)

  db_list = []
  for u in q:
    db_list.append(Dummy(u.choreographer, u.dancers))
  return db_list


if __name__ == '__main__':  
  def test_add_pieces():
    pieces = {'anna@college': ['d'], 'fd': ['dfa'], 'ddd': ['dfa', 'fdsaf']}
    add_pieces(pieces)
    print("added pieces")
    show_pieces()


  #
  #test_del_users()
  #test_update_users()
  #clear_table()
  #test_add_users()
  #show_users()
  #lst = get_user_data_list()
  #choreo = get_choreographers(lst)
  #names = [d.firstname for d in choreo]
  #print (names)
  test_add_pieces()
