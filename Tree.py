import helper

#MAKE SEARCH TREE
class Node:
	def __init__(self, name, time, successors = None, path = []):
		self.name = name
		self.time = time
		self.successors = successors
		self.path = path

	def add_path(self, old_path, node):
		self.path = old_path[:]
		self.path.append(node.time)

	def add_successors(self, successors):
		self.successors = successors

def makeTree(pieces):
	#create start node
	start = Node('start', None)
	current = [start]
	#order the domain 
	ordered = helper.time_counts(pieces)
	number_nodes = 1
	for p in helper.order(pieces):
		successors = []
		times = sorted(p.times, key = lambda x: ordered[x])
		for t in times:
			new_node = Node(p.choreographer, t)
			successors.append(new_node)
		for c in current:
			c.add_successors(successors)
		number_nodes *= len(successors)
		current = successors
	print ('This tree has a total of {} nodes to explore'.format(number_nodes))
	return start