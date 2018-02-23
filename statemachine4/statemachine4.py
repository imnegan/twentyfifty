

class StateMachine:

	def __init__(self, transitionData):

		'''
		- Get states
		- Get transitions
		- Link functions 
		'''
		#Get states
		self.states={}
		for row in transitionData:
			for stateName in row[:2]:
				self.states[stateName]=State(self, stateName)
		#Set initial state
		self.state=self.states[transitionData[0][0]]
		
	def onEvent(self, event):
		self.state.onEvent(event)
		
class State:
	
	def __init__(self, stateMachine, name):
		self.stateMachine=stateMachine
		self.name=name
		
	def onEvent(self, event):
		pass