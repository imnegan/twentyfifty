from collections import defaultdict, namedtuple
import logging

from event import *

def listify(obj):
	'''from transitions repo'''
	if obj is None:
		return []
	else:
		return obj if isinstance(obj, (list, tuple, type(None))) else [obj]
		
class StateMachine(EventControllerMember):

	#transitionData=[[fromState, toState, conditions, negations, actions]]

	def __init__(self, eventController, transitionData):
	
		self.state=transitionData[0][0]
		self.lastState=None
		self.states=defaultdict(set)
		
		for row in transitionData:
			#if row[0]!='*':
			self.states[row[0]].add(Transition(*row))
			
		EventControllerMember.__init__(self, eventController)
		
	def defaultCondition(self, event):
		logging.error('defaultCondition')
		return False
		
	def defaultAction(self, event):
		logging.error('defaultAction')
		
	def defaultNegation(self, event):
		logging.error('defaultNegation')
		return False
		
	def onEvent(self, event):
		for t in self.states[self.state]:
			if getattr(self, t.conditions, self.defaultCondition)(event):
				getattr(self, t.actions, self.defaultAction)(event)
				self.lastState=self.state
				self.state=t.toState
				#TODO: post transition event
				#self.ec.post(Event(transition=t))
				break
				
Transition=namedtuple('Transition', ['fromState', 'toState', 'conditions', 'negations', 'actions'])
Transition.__new__.__defaults__ = (None, None, None)

# --- testing ground

class TestSM(StateMachine):

	transitionData=[
	['s1', 's2', 'condition', None, 'action'],
	['s2', 's1', 'condition', None, 'action'],
	['*', 's1', 'condition']
	]
	
	def __init__(self, eventController):
		StateMachine.__init__(self, eventController, TestSM.transitionData)
		
	def condition(self, event):
		print('condition is True')
		return True
		
	def action(self, event):
		print('Action!')
		
def test():
	ec=EventController()
	tsm=TestSM(ec)
	print(tsm.state)
	
	for i in range(4):
		print('start', tsm.state)
		tsm.onEvent(object)
		print('end', tsm.state,'\n')
		
	print(tsm.lastState)
	print(tsm)
	
if __name__== '__main__':
	logging.info('Running stateMachine.py directly.')
	test()
else:
	logging.info('stateMachine.py loaded.')

