
import helper
import Tree
import random, math


class Scheduler:
	def __init__(self, dancers, pieces, domain, violations = []):
		self.dancers = dancers
		self.pieces = pieces
		self.domain = domain
		self.violations = violations

	def set_initial(self, pieces, dancers):
		for p in pieces:
			for d in p.performers:
				p.times = helper.crossOff(p.times, d.availability)
		
	def set_times(self, pieces):
		#iterate through the remaining times in each rehearsal
		#naively assign the first times
		for p in pieces:
			if p.times:
			#set rehearsal time to the first time
				p.slot = p.times[0]
			for x in pieces:
				if p.slot in x.times:
					x.times.remove(p.slot)
		return True
	
	#USING HEURISTIC
	def heuristic(self, pieces):
		ordered = helper.order(pieces)
		names = [x.choreographer.name for x in ordered]
		print ("the order of assignments is {}".format(names))
		while ordered:
			MRV = ordered[0]
			counts = helper.time_counts(ordered)
			values = [(x, counts[x]) for x in MRV.times]
			ordered = helper.order(ordered[1:])
			while len(values) != 0:
				#find the least constraining value
				LCV = min(values, key=lambda x: x[1])
				MRV.slot = LCV[0]
				if helper.check(ordered, MRV.slot):
					for x in ordered:
						if MRV.slot in x.times:
							x.remove_time(MRV.slot)
					#go to assigning the next piece
					break
				else:
					#go to the next least constraining value
					MRV.slot = None
					values.remove(LCV)
					#if no more values remain
					if not values:
						print ("Unable to assign time slot to {} rehearsal".format(MRV.choreographer.name))
						return False
		return True

	#DEPTH FIRST SEARCH
	def DFS(self, pieces):
		#make search tree
		start_node = Tree.makeTree(pieces)
		if not start_node:
			return False
		solutions = []
		sol_scores = []
		#traverse tree
		stack = [start_node]
		while stack:
			#print ('stack', len(stack))
			vertex = stack.pop()
			if vertex.successors:
				for child in vertex.successors:
					#need to a check that the child is not contained in the path before
					if child.time not in vertex.path:
						#update the childs path
						child.add_path(vertex.path, child)
						#add the child to the stack
						stack.append(child)
			#if at the deepest level in tree (no children)
			else:
				solutions.append(vertex.path)
				#self.assign_solution(vertex.path)
				self.set_slots(solution = vertex.path)
				score = self.evaluate()
				sol_scores.append((vertex.path, score))

		if not solutions:
			print ('no valid assignment found')
			return False

		best = max(sol_scores, key=lambda x: x[1])[0]
		self.set_slots(solution = best)
		return True

	def get_violations(self):
		self.violations = []
		for p in self.pieces:
			for d in p.performers:
				if p.slot not in d.availability:
					self.violations.append((d.name,p))

	def random_SA(self, pieces):
		#reset
		for p in pieces:
			p.times = p.choreographer.availability

		#assign times randomly as start
		ordered = helper.order(pieces)
		for i, p in enumerate(ordered):
			p.slot = random.choice(p.times)
			for x in ordered[i+1:]:
				if p.slot in x.times:
					x.times.remove(p.slot)
		self.set_slots()
		self.get_violations()

		def assign_to_neighbor(piece):
			slot = helper.get_min_conflict_time(self,piece)
			if slot:
				piece.slot = slot

		def run(T, schedule):
			accepted = []
			while T > 1:
				current_value = len(self.violations)
				if current_value == 0:
					return True
				rand_piece = random.choice(self.violations)[1]
				old = rand_piece.slot
				assign_to_neighbor(rand_piece)
				self.set_slots()
				self.get_violations()
				new_value = len(self.violations)
				delta = -(new_value - current_value)
				if delta > 0:
					accepted.append(new_value)
				else:
					if random.random() < math.exp(delta / float(T)):
						accepted.append(new_value)
					else:
						rand_piece.slot = old
						self.set_slots()
						self.get_violations()
			
				T *= schedule
			print (accepted)

		run(10000, 0.90)
		return True

	def relax_constraints_after(self, randomness):

		size_domains = [(len(p.times),p) for p in self.pieces]
		MRV = min(size_domains, key = lambda x: x[0])[1]
		if randomness:
			if random.random() > 0.8:
				MRV = random.choice(self.pieces)

		most_constraining_dancer = helper.find_most_constraining(MRV)
		MRV.remove_dancer(most_constraining_dancer)
		self.violations.append((most_constraining_dancer.name, MRV))
		MRV.times = [x for x in MRV.choreographer.availability if x in self.domain]
		self.set_initial(self.pieces, self.dancers)

	def set_slots(self, solution = None, actual = None):
		if solution: 
			for p, time in zip(helper.order(self.pieces), solution):
				p.slot = time
		if actual:
			for p in self.pieces:
				#print (p.choreographer.name)
				p.slot = actual[p]
		for d in self.dancers:
			d.times = []
			d.pieces = []
			for p in self.pieces:
				if d in p.performers:
					d.times.append(p.slot)
					d.pieces.append(p.choreographer.name)
			#print ('d.times', d.times)
			d.times = sorted(d.times, key = lambda x: (x.split('.')[0], int(x.split('.')[1])))
	#try to maximize evaluation score
	def evaluate(self):
		#nonharvard students have their rehearsals on the same day
		nonharvard_score = 0
		#check for dinner breaks
		dinner_score = 0
		#check for super late rehearsals (11 pm)
		late_score = 0
		#check that rehearsals are clustered together
		cluster_score = 0
		for d in self.dancers:
			if d.nonharvard:
				days = [x.split('.')[0] for x in d.times]
				if len(set(days)) == 1:
					nonharvard_score += 3
				#minimize the time difference
			ind_score = 0
			if d.times:
				for i,t in enumerate(d.times[:-1]):
					if t.split('.')[0] == d.times[i+1].split('.')[0]:
						if abs(int(t.split('.')[1]) - int(d.times[i+1].split('.')[1])) < 2:
							ind_score += 1
							#print ('ind', ind_score)
				cluster_score += (ind_score/len(d.times))
			hours = [int(x.split('.')[1]) for x in d.times]
			if not(5 in hours and 6 in hours):
				dinner_score += 1

		for p in self.pieces: 
			print ('p.slot', p.slot)

		times = [int(p.slot.split(',')[1]) for p in self.pieces]
		late = [x for x in times if x > 10]
		if not late:
			late_score += 1
		return nonharvard_score + dinner_score + late_score + cluster_score


def relax_constraints_before(problem, invalid_pieces):
#remove dancers with smallest overlap
	for p in invalid_pieces: 
		if p.performers:
			while not p.times:
				most_constraining_dancer = helper.find_most_constraining(p)
				p.remove_dancer(most_constraining_dancer)
				problem.violations.append((most_constraining_dancer.name, p))
				p.times = [x for x in p.choreographer.availability if x in problem.domain]
				problem.set_initial(problem.pieces, problem.dancers)
		else:
			p.choreographer.availability = problem.domain
			p.times = p.choreographer.availability
			problem.set_initial(problem.pieces, problem.dancers)
		
