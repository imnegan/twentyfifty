class State:
	def __init__(self, name):
		self.name=name
		self.transitions=[]
		
	def __eq__(self, other):
		return self.name==other
		
	def __repr__(self):
		return self.name
		
	def __hash__(self):
		return hash(str(self.__dict__))
		
class Transition:
	def __init__(self, name, fromState, toState, condition, action=None):
		self.name=name
		self.fromState=fromState
		self.toState=toState
		self.condition=condition
		if action is None:
			self.action='passAction'
		else:
			self.action=action

	def __eq__(self, other):
		return self.name==other

class StateMachine:
	def __init__(self, name, states, transitions, initialState):
		self.name=name
		self.states=set()
		
		for state in states: self.addState(state)
		i=State(initialState)
		self.addState(i)
		self.state=i

	def addState(self, state): 
		self.states.add(State(state))
		
	def addTransition(self, transition): pass
		
	
	def passAction(self): pass
			
states=['a', 'b', 'c']
transitions=['aTOb', 'bTOc', 'cTOa']
initialState='a'
sm=StateMachine('state machine', states, transitions, initialState)


		
print('fin')