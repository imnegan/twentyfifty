import logging

class StateMachine:

	def __init__(self, transitionData):

		'''
		- Get transitions
		- Link functions 
		'''
		#Get states
		self.states={}
		for row in transitionData:
			for stateName in row[1:3]:
				if stateName != '=' and stateName != '*':
					self.addState(stateName)
		#Set initial state
		self.state=self.states[transitionData[0][0]]
		#Add transitions
		for row in transitionData:
			Transition(self, *row)
		
	def addState(self, stateName):
		self.states[stateName]=State(self, stateName)
		
	def onEvent(self, event):
		self.state.onEvent(event)
	
	def defaultFunc(self, event):
		logging.error('Function not found')
		return false
	
	# ---[conditions

	
	# ---[actions

class State:
	
	def __init__(self, stateMachine, name):
		self.stateMachine=stateMachine
		self.name=name
		self.transitions={}
		
	def addTransition(self, transition):
		self.transition[transition.name]=transition
		
	def onEvent(self, event):
		pass


class Transition:

	#[name, fromState, toState, conditions, actions]
	
	def __init__(self, stateMachine, name, fromState, 
		toState, conditions, actions=None):
		
		self.stateMachine=stateMachine
		
		self.name=name
		self.stateMachine.states[fromState].addTransition(self)
		self.toState=self.stateMachine.states[toState]
		self.conditions=set()
		self.actions=set()
		
		self.addFunctions(conditions, self.conditions)
		self.addFunctions(actions, self.actions)
		
	def addFunctions(strInput, funcSet):
		if strInput is not None and strInput != '':
			strInput=list(strInput)
			for s in strInput:
				funcSet.add(self.stateMachine.getattr(self.stateMachine, s, self.stateMachine.defaultFunc))
	
