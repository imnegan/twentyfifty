from event import *
from collections import defaultdict
import logging

#transitions=[trigger, source(s), destination, conditions, negations, before, after, prepare]

class StateMachine: 

	def __init__(self, transitionsData):
		
		self.states=set()
		self.state=None
		self.setInitialState() 
		
	def populateStates(self):
		''' add all states from the source and destination fields in the transitions data'''
		pass
		
	def setInitialState(self):
		''' set to the fromState from the first transition '''
		pass
		
	X
	def run(self, event):
		changeState=True
		while changeState is True:
			for condition in self.transitions[self.state].conditions:
				if len
				changeState=condition()'''
		
	# ---[condition/negation functions
	
	# ---[before/after/prepare action functions
		

class State: pass

class Transition:
	
	def __init__(self, stateMachine, source, destination, conditions=None, negations=None, before=None, after=None, prepare=None):
		
		self.stateMachine=stateMachine
		self.source=source
		self.destination=destination
		logging.debug('Loading conditions...')
		self.conditions=self.setFunctions(conditions)
		logging.debug('Loading negations...')
		self.negations=self.setFunctions(negations)
		logging.debug('Loading before functions...')
		self.before=self.setFunctions(before)
		logging.debug('Loading after functions...')
		self.after=self.setFunctions(after)
		logging.debug('Loading prepare functions...')
		self.prepare=self.setFunctions(prepare)
	
	def run(self):
		
		#https://github.com/pytransitions/transitions#-execution-order
		
		logging.debug()
		
	def setFunctions(self, funcNames):
		funcList=list(funcNames)
		try: funcList=list(funcNames)
		except: 
			logging.error('None loaded. ')
			funcList=[]
		result=set()
		for funcName in funcList:
			msg="Loading funcName '"+str(funcName)+"..."
			logging.debug(msg)
			try:
				func=getattr(self.stateMachine, funcName)
				result.add(func)
			except:
				msg="Couldn't load funcName '"+str(funcName)+"''."
				logging.error(msg)
		return result
		
		
# ---[testing ground
class dummy:
	def a(self):
		print('a')
	def b(self):
		print('b')
	def c(self):
		print('c')


