from db_manager import *
from helper_db import *

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
    del_user('ADMIN')  
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
    admin =  {'email': 'harvardballetcompany@gmail.com', 'firstname': 'BALLERina93', 'lastname': '', 'nonharvard': False, 'choreographer': False}
    add_user(admin)
    show_users()

  def test_avail():
    user_avails = [(x.firstname, x.lastname, get_availability(x.username)) for x in get_user_data_list()]
    print (user_avails)

  def test_domain():
    print (get_domain())
  def test_castlist():
    print (get_castlist())

  #test_avail()
  #test_update_example()
  #test_domain()
  #test_add_example()
  #add_admin()
  #test_update_users()
  #clear_table()
  #test_add_users()
  #user_update('anna@college', '2017-10-16,4;2017-10-16,5;2017-10-16,6;2017-10-16,7;2017-10-16,8;2017-10-16,9;2017-10-16,10;2017-10-16,11;2017-10-17,11;2017-10-18,11;2017-10-19,11;2017-10-20,11;')
  show_users()
  #test_add_pieces()
  #get_availability('anna@college')
  #test_del_users()
  #test_castlist()