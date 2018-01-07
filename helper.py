
#HELPER FUNCTIONS FOR SCHEDULER

def eval(function, *args):
	return (function(*args))

def crossOff(rehearsal_times, dancer_times):
	#Removes unavailable dancer times from rehearsal times
	#dancer times is a list of dancer's available times
	#rehearsal times is the list of the choreographer's available times
	print ('crossing off')
	new_rehearsal_times = rehearsal_times[:]
	for r in rehearsal_times:
		if r not in dancer_times:
			print ('removed time')
			new_rehearsal_times.remove(r)
	return new_rehearsal_times

#checks if there empty domains
def check_empty(problem):
	empty_domain = []
	for p in problem.pieces:
		if not p.times:
			empty_domain.append(p)
	return empty_domain

#finds most contraining dancer in the piece
def find_most_constraining(piece):
	#count the overlap between the choreographer's availabiity and the dancer's availabiity
	performer_overlap = []
	for d in piece.performers:
		overlap = list(set(d.availability).intersection(piece.choreographer.availability))
		performer_overlap.append((d, len(overlap)))
	most_constraining_dancer = (min(performer_overlap, key = lambda x: x[1]))[0]
	return most_constraining_dancer

#arc consistency check if no legal values remain in rest of pieces
def check(pieces, slot):
	for p in pieces:
		if slot in p.times:
			if len(p.times) == 1:
				return False
	return True

def order(pieces):
	ordered = sorted(pieces, key=lambda x: len(x.times))
	return ordered

#sort times to find least constraining value
def time_counts(pieces):
	counts = {}
	for p in pieces:
		for t in p.times:
			if t in counts:
				counts[t] += 1
			else:
				counts[t] = 1
	return counts


def get_min_conflict_time(problem, piece):
	#get possible times for piece
	times = [x for x in piece.choreographer.availability if x in problem.domain]
	for p in problem.pieces:
		if p != piece: 
			if p.slot in times:
				times.remove(p.slot)
	#count constraints involving each time
	time_conflicts = []
	for t in times:
		conflicts = 0
		for p in problem.pieces:
			if t in p.times:
				conflicts+= 1
		time_conflicts.append((t, conflicts))
	time_conflicts = sorted(time_conflicts, key = lambda x: x[1])
	#count violations involving each time
	counts = []
	for t in time_conflicts:
		count = 0
		for d in piece.performers:
			if t[0] in d.availability:
				count += 1
		counts.append((t[0], count))
	if counts:
		#return the time with lowest violations and constraints
		best_time = max(counts, key  = lambda x: x[1])[0]
		return best_time
	else:
		return None

#gets busiest dancer
def get_dancer_counts(problem):
	dancers = {}
	for p in problem.pieces:
		for d in p.performers:
			if d in dancers:
				dancers[d].append(p)
			else:
				dancers[d] = [p]
