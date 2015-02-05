import rubik

def shortest_path(start, end):
	"""
	Using 2-way BFS, finds the shortest path from start_position to
	end_position. Returns a list of moves. 

	You can use the rubik.quarter_twists move set.
	Each move can be applied using rubik.perm_apply
	"""
	
	class node:
		def __init__(self):
			self.permutation=None
			self.parent=None
			self.level=None
			self.operation=None
			#self.discovered=None
			self.compared=None

	m=10007
	start_parents=[]
	end_parents=[]
	start_queue=[]
	end_queue=[]
	moves=[]
	hash_table_main=[[] for i in range(m)]
	hash_table_start=[[] for i in range(m)]
	hash_table_end=[[] for i in range(m)]

	def hash_fn(t):
		'''returns a hash value for a particular configuration'''
		x=0
		sum1=0
		gamma=0.61803398875
		for i in t:
			sum1=sum1+(i*(2**x))
			x+=1
		sum1=sum1%m
		# sum1=sum1*gamma
		# sum1=sum1%1
		# sum1=int(sum1*m)
		return sum1

	def perm_inv(operation):
		'''Gives the inverse permutation of a permutation'''
		if operation==rubik.quarter_twists[0]:
			x=1
		elif operation==rubik.quarter_twists[1]:
			x=0
		elif operation==rubik.quarter_twists[2]:
			x=3
		elif operation==rubik.quarter_twists[3]:
			x=2
		elif operation==rubik.quarter_twists[4]:
			x=5
		else:
			x=4
		return x


	def BFS(q):
		'''Performs a breadth first search and gives the neighbouring nodes of a node not already compared'''
		hash_table=[[] for i in range(m)]
		l=len(q)
		for x in range(l):
			vertex=q.pop(0)
			for i in range(6):
				flag=0
				a=node()
				a.permutation=rubik.perm_apply(rubik.quarter_twists[i],vertex.permutation)
				hv=hash_fn(a.permutation)
				for element in hash_table_main[hv]:
					if element.permutation==a.permutation:
						flag=1

				if flag==0:
					a.parent=vertex
					a.level=vertex.level+1
					a.operation=rubik.quarter_twists[i]
					a.compared=0
					q.append(a)
					hv=hash_fn(a.permutation)
					hash_table[hv].append(a)
		return hash_table


	'''The shortest_path starts from here'''
	if start==end:
		return moves

	else:
		start_node=node()
		start_node.level=0
		start_node.permutation=start
		start_queue.append(start_node)
		hv=hash_fn(start_node.permutation)
		hash_table_main[hv].append(start_node)
		hash_table_start[hv].append(start_node)
		
		end_node=node()
		end_node.level=0
		end_node.permutation=end
		end_queue.append(end_node)
		hv=hash_fn(end_node.permutation)
		hash_table_end[hv].append(end_node)
		run=0
		while run<7:
			hash_table_start=BFS(start_queue)
			for element in end_queue:
				hv=hash_fn(element.permutation)
				hash_table_main[hv].append(element)
			#print len(start_queue)
			m=len(hash_table_start)
			for perm_s in start_queue:
				hv=hash_fn(perm_s.permutation)
				for perm_e in hash_table_end[hv]:
					if perm_s.permutation==perm_e.permutation:
						#print len(hash_table_end[hv])
						while perm_s!=None:
							if perm_s.operation!=None:
								moves.insert(0,perm_s.operation)
							perm_s=perm_s.parent
						#perm_e=perm_e.parent
						while perm_e!=None:
							if perm_e.operation!=None:
								x=perm_inv(perm_e.operation)
								moves.append(rubik.quarter_twists[x])
							perm_e=perm_e.parent
						return moves

			hash_table_end=BFS(end_queue)
			for element in start_queue:
				hv=hash_fn(element.permutation)
				hash_table_main[hv].append(element)
			m=len(hash_table_end)
			for perm_e in end_queue:
				hv=hash_fn(perm_e.permutation)
				for perm_s in hash_table_start[hv]:
					if perm_s.permutation==perm_e.permutation:
						#perm_s=perm_s.parent
						while perm_s!=None:
							if perm_s.operation!=None:
								moves.insert(0,perm_s.operation)
							perm_s=perm_s.parent
						while perm_e!=None:
							if perm_e.operation!=None:
								x=perm_inv(perm_e.operation)
								moves.append(rubik.quarter_twists[x])
							perm_e=perm_e.parent
						return moves
			run+=1