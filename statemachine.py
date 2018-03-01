from collections import defaultdict, namedtuple
import logging, csv, os

from event import *

def getTransitionsFromCsv(filename):
	
	main_dir = os.path.split(os.path.abspath(__file__))[0]
	csvfile = open(os.path.join(main_dir, filename))
	
	reader = csv.DictReader(csvfile)
	transitions=[]
	
	for row in reader:
		drow=dict(row) #dict row
		for k, v in drow.items():
			if v=='None' or v=='':
				drow[k]=None
		transitions.append(drow)
		#print(drow)
	
	return transitions

def listify(obj):
	'''from transitions repo'''
	if obj is None:
		return []
	else:
		return obj if isinstance(obj, (list, tuple, type(None))) else [obj]
		
class StateMachine(EventMember):

	#transitionData=[[name, fromState, toState, conditions, negations, actions]]

	def __init__(self, eventController, transitionData):
	
		self.state=transitionData[0][1]
		self.lastState=None
		self.states=defaultdict(set)
		
		for row in transitionData:
			#if row[0]!='*':
			self.states[row[1]].add(Transition(*row))
			
		EventMember.__init__(self, eventController)
		
	def testConditionsAndNegations(self, event, conditions, negations):
		result=True
		for condition in listify(conditions):
			logging.debug('...'+condition+' is '+str(getattr(self, condition, self.defaultCondition)(event)))
			result=result and getattr(self, condition, self.defaultCondition)(event)
		for negation in listify(negations):
			result=result and not getattr(self, negation, self.defaultNegation)(event)
		logging.debug('...testConditionsAndNegations is '+str(result))
		return result
		
	def runActions(self, event, actions):
		for action in listify(actions):
			getattr(self, action, self.defaultAction)(event)
		
	def defaultCondition(self, event):
		logging.error('defaultCondition')
		return False
		
	def defaultAction(self, event):
		logging.error('defaultAction')
		
	def defaultNegation(self, event):
		logging.error('defaultNegation')
		return True
		
	def onEvent(self, event):
		for s in '*', self.state:
			for t in self.states[s]:
				if self.testConditionsAndNegations(event, t.conditions, t.negations):
					self.runActions(event, t.actions)
					self.lastState=self.state
					self.state=t.toState
					self.post(Event(type='transition'))
					break
				
Transition=namedtuple('Transition', ['name', 'fromState', 'toState', 'conditions', 'negations', 'actions'])
Transition.__new__.__defaults__ = (None, None, None)

# --- testing ground

class TestSM(StateMachine):

	transitionData=[
	['s12', 's1', 's2', 'condition', None, 'action'],
	['s21', 's2', 's1', 'condition', None, 'action'],
	['s*-idle', '*', 'idle', None, 'condition'],
	['idling', 'idle', 'idle']
	]
	
	def __init__(self, eventController):
		self.count=0
		StateMachine.__init__(self, eventController, TestSM.transitionData)

		
	def condition(self, event):
		logging.debug('start state'+self.state)
		if event.type=='tick' and self.count<10:
			logging.debug('condition is True')
			return True
		else: 
			logging.debug('condition is False')
			return False
		
	def action(self, event):
		self.count+=1
		logging.debug('Action!'+str(self.count))
		self.post(Event(type='tick'))
		
def test():
	ec=EventController()
	tsm=TestSM(ec)
	
	
	ec.post(Event(type='tick'))
	
	print(tsm.states)
	'''
	print(tsm.state)
	
	for i in range(4):
		print('start', tsm.state)
		tsm.onEvent(Event(type='tick'))
		print('end', tsm.state,'\n')
		
	print(tsm.lastState)
	print(tsm)
	'''
	
if __name__== '__main__':
	logging.info('Running stateMachine.py directly.')
	test()
else:
	logging.info('stateMachine.py loaded.')

