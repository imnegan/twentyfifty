# (c)Paul Egan 2018
import csv, os, logging
from collections import defaultdict



def getTransitionsFromCsv(filename):
	
	main_dir = os.path.split(os.path.abspath(__file__))[0]
	csvfile = open(os.path.join(main_dir, filename))
	
	reader = csv.DictReader(csvfile)
	transitions=[]
	
	for row in reader:
		drow=dict(row) #dict row
		transitions.append(drow)
		print(drow)
	
	return transitions

class StateMachine:
	
	def __init__(self, transitions, initialState=None):
		
		self.states=defaultdict(set)
		self.state=None
		self.lastState=None
		
		for t in transitions:
			transition=Transition(self, **t)
			self.states[transition.fromState].add(transition)
			#set the initial state
			if self.state is None:
				self.state=transition.fromState
		
	def run(self):
		logging.warning('Running: '+self.state)
		for t in self.states[self.state]:
			logging.warning('Testing transition: '+t.name)
			result=t.condition()
			logging.warning(result)
			if result == True:
				if hasattr(t, 'action'):
					t.action()
					logging.warning('Running action.')
				else: logging.warning('No action to run.')
				self.state=t.toState
				logging.warning('transitioned to:'+self.state)
				break
			
	#Condition & negation functions
	def defaultCondition(self):
		logging.error('defaultCondition')
		return False
	
	'''	
	def defaultNegation(self):
		logging.error('defaultNegation')
		return True
	'''
	
	#Action & postAction functions
	def defaultAction(self):
		logging.error('defaultAction')
	
	'''	
	def defaultPostAction(self):
		logging.error('defaultPostAction')
	'''

class Transition:
	
	def __init__(self, stateMachine, name=None, fromState=None, toState=None, condition=None, action=None): #, negations=None, postActions=None):
		
		self.stateMachine=stateMachine
		self.name=name
		
		self.fromState=fromState
		self.toState=toState
		
		stateMachine.states[fromState].add(self)
		
		self.condition=getattr(stateMachine, condition, stateMachine.defaultCondition)
		#if condition function is true the state is changed to the target state
		
		#self.negations=negations #negative conditions 'not condition'
		
		if action != None:
			self.action=getattr(stateMachine, action, stateMachine.defaultAction)
		else:
			logging.warning('no action added')
		#actions run before the transition
		
		#self.postActions=postActions #actions run after the transition
		
	def __repr__(self):
		return str(self.name)
		

if __name__ == "__main__":
	
	#Logging
	import logging
	logging.basicConfig(level=logging.NOTSET)
	logging.warning('statemachine.py is being run directly')
	
else:
	logging.debug('statemachine.py loaded.')
		
