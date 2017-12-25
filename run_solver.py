import user_manager as um
from classes import Dancer, Rehearsal

all_users = um.get_user_data_list()
all_dancers = []


all_pieces = []

for u in all_users:
	all_dancers.append(Dancer(u.name, u.availability, u.nonharvard, u.choreographer))







