from scheduler import *
import user_manager as um
import helper
from classes import *

### get Dancer objects
def get_dancers():
    dancers = [Dancer(d.firstname+d.lastname, d.availability.split(';'), d.nonharvard, d.choreographer) for d in um.get_user_data_list()]
    return dancers

### get Rehearsal objects
def get_pieces(dancers, domain):
    choreographers = [(Dancer(d.firstname+d.lastname, d.availability.split(';'), d.nonharvard, d.choreographer), 
        d.dancers) for d in um.get_user_data_list() if d.choreographer]
    pieces = []
    for c in choreographers:
        performers = []
        for p in c[1].split(', '):
            performers.append(um.search_user(p))
        pieces.append(Rehearsal(c[0], performers, domain))
    return pieces


def solve(domain):
    dancers = get_dancers()
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
    domain = "2017-12-06,4;2017-12-06,5;2017-12-06,6;2017-12-06,7;2017-12-06,8;2017-12-06,9;2017-12-06,10"
    def test_get_dancers():
        for item in get_dancers():
            print (item.name)

    def test_get_pieces():
        dancers = um.get_user_data_list()
        pieces = get_pieces(dancers, domain)
        print ('lengthh of pieces', len(pieces))
        for item in pieces:
            print (item.choreographer)
            print (item.performers)

    def test_solve():
        solve(domain)

    #test_get_dancers()
    #test_get_pieces()
    test_solve()




