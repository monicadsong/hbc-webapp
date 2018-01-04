from scheduler import *
import user_manager as um
import helper


### get Dancer objects
def get_dancers():
	dancers = [Dancer(d.firstname+d.lastname, d.availability, d.nonharvard, d,choreographer) for d in um.get_user_data_list()]
	return dancers

### get Rehearsal objects
def get_pieces(choreographers, domain):
	pieces = [Rehearsal(c.firstname+c.lastname, c.dancers, domain) for c in choreographers]


def solve():
	domain = get_domain()
	dancers = get_dancers()
	pieces = get_pieces(um.get_choreographers, domain)
	problem = Scheduler(dancers, pieces, domain)
	problem.set_initial(pieces, dancers)
	invalid_pieces = helper.check_empty(problem)
	if invalid_pieces:
		relax_constraints_before(problem, invalid_pieces)
		print ("num of violations", len(problem.violations))


	algo = {
	'naive': problem.set_times,
	'heuristic': problem.heuristic,
	'DFS': problem.DFS,
	'random': problem.random_SA
	}
	

	output = helper.eval(algo[algorithm], pieces)
	while not output:
		problem.relax_constraints_after(randomness)
		output = helper.eval(algo[algorithm], pieces)

	problem.set_slots()
	score = problem.evaluate()

	for p in pieces:
		if p.slot:
			print ("the assigned time for {} piece is {}".format(p.choreographer.name, p.slot))
		else:
			print ("Unable to assign time slot to {} rehearsal".format(p.choreographer.name))

	for d in dancers:
		if d.times:
			print ("{} has these times scheduled: {}".format(d.name, d.times))

	print ('This solution has {} violations'.format(len(problem.violations)))
	if problem.violations:
		for v in problem.violations:
			print ("{} cannot attend {}'s piece at {}".format(v[0], v[1].choreographer.name, v[1].slot))
	print ('Score: {}'.format(score))



