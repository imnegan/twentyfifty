class StateMachine:

	#transitions=[trigger, source(s), destination, conditions, negations, before, after, prepare]
	transitionData=( #trigger, source(s), destination, conditions, unless, before, after, prepare]
		('fossicking', 'mining', 'foundOre'),
		('mining', 'mining', None, 'isFull', 'mine'),
		('mining', 'returning', 'isFull'),
		('returning', 'unloading'),
		('unloading', 'unloading', None, 'isEmpty', 'unload'),
		('unloading', 'fossicking', 'isEmpty'))

	def __init__(self):
		
		self.state=StateMachine.transitionData[0][0]
		self.states=set([row[0] for row in StateMachine.transitionData])
		self.states=self.states.union(set([row[1] for row in StateMachine.transitionData]))
		self.states.discard('=')
		self.states.discard('*')
		print(self.state)
		print(self.states)

	def run(self, event):
		
		for transition in self.state.transitions:
			
			makeTransition=True
			
			while makeTransition==True:
			
				#prepare actions
				try:
					for prepare in list(transition.prepare):
						getattr(self, prepare)(self, event)
				except: pass
				
				#test conditions
				try:
					for condition in list(transition.conditions):
						makeTransition = getattr(self, condition)(self, event)
						if makeTransition is False: break
				except: pass
				
				#test negations
				try:
					for negation in list(transition.negations):
						makeTransition = not getattr(self, negation)(self, event)
						if makeTransition is False: break
				except: pass
				
				#before actions
				try:
					for before in list(transition.before):
						getattr(self, before)(self, event)
				except: pass
				
				#make transition
				self.state=transition.destination
				
				#after actions
				try:
					for after in list(transition.after):
						getattr(self, after)(self, event)
				except: pass
				
			break
			
s=StateMachine()
