

class Node:
	def __init__(self,data):
		self.data = data
		#self.nex_node = None
		self.prev_node = None



class Generator:
	def __init__(self, range_list):
		self.root = None
		self.leaves = []
		self.counter = 0
		self.states = {}

		#build tree on init function 
		self.build_tree(range_list, None)

		#get all paths and update counter
		self.get_all_paths()
	
	def append(self, prev_state, data):
		#create new state
		#self.nodes_counter = self.nodes_counter + id
		new_state = Node(data)
		
		#check if path root is None (it means theresn't a root path already set)
		#here prev_state would be None, because is the first node without a previous node
		#print('prev node id: ', new_state.id)
		if self.root == None:
			#if there is not a root path already set, asign state as root node
			self.root = new_state
			return new_state
		else:
			#if root node already exist then next nodes have to reference to prev node because is a reverse reference
			#the new state we are creating is referenced to the previous one 
			new_state.prev_node = prev_state
			return new_state

		#print elements of linked list
	def print_backward_path(self, leaf):
		combination_state = []
		current_node = leaf
		while current_node != None:
			#print(current_node.data)
			combination_state.append(current_node.data)
			current_node = current_node.prev_node
		
		return combination_state
		
	
	def build_tree(self, range_list, node_to_append):
	#copy list and delete first element
		reduced_list = range_list[:]
		if len(reduced_list) != 0:
			reduced_list.pop(0)
		#reduced_list = [[0,1,2], [0,1], [0,1]]
		for list in range_list:
			for element in list:
				current_node = self.append(node_to_append, element)
				#check if we are adding a root node (leaf)
				if len(range_list) == 1:
					#if is a leave then add to tree leaves list
					self.leaves.append(current_node)
				#por cada elemento creado, ahora llamar funcion recursiva para agregarle un nodo del siguien
				#elemento de range_list y así a cada uno de estos añadir el siguiente nivel, hasta terminar
				#recall recursive function
				self.build_tree(reduced_list, current_node)
			#exit from second for break first for
			break
			
			
	def get_all_paths(self):
		counter = 0
		for leaf in self.leaves:
			combination = self.print_backward_path(leaf)
			hash_str_list = [str(int) for int in combination]
			hash_str = ",".join(hash_str_list)
			self.states[hash_str] = combination
			#print('-----------------------')
			counter = counter + 1
		print(counter)
		self.counter = counter
		print(self.states)

#range_list = [[0,1], [0,1,2], [0,1], [0,1],  [0,1,2,3]]
#range_list = [[0,1,2],[0,1], [0,1], [0,1], [0,1], [0,1], [0,1]]
#new_tree = Generator()
#build_tree(range_list, new_tree, None)

#get_all_paths(new_tree)