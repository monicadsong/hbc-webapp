from scheduler import *
import db_manager as dm
import helper
from classes import *

### get Dancer objects
def get_dancers():
    dancers = [Dancer(d.firstname+d.lastname, d.availability.split(';'), d.nonharvard, d.choreographer) for d in dm.get_user_data_list()]
    return dancers

### get Rehearsal objects
def get_pieces(dancers, domain):
    choreographers = [(Dancer(d.firstname+d.lastname, d.availability.split(';'), d.nonharvard, d.choreographer), 
        d.dancers) for d in dm.get_user_data_list() if d.choreographer]
    domain = domain.split(';')
    pieces = []
    for c in choreographers:
        performers = []
        for p in c[1].split(', '):
            performers.append(dm.search_user(p))
        pieces.append(Rehearsal(c[0], performers, domain))
    return pieces

def solve():
    dancers = get_dancers()
    domain = dm.get_domain()
    pieces = get_pieces(dancers, domain)
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
    
    algorithm = 'heuristic'

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

    return pieces, problem.violations



if __name__ == '__main__':  
    def test_get_dancers():
        for item in get_dancers():
            print (item.name)

    def test_get_pieces():
        domain = dm.get_domain()
        dancers = dm.get_user_data_list()
        pieces = get_pieces(dancers, domain)
        for item in pieces:
            print (item.choreographer)
            print (item.performers)

    def test_solve():
        solve()

    #test_get_dancers()
    #test_get_pieces()
    #test_solve()





