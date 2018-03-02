from statemachine import StateMachine
from event import *

class Container(StateMachine):
	
	states=['empty', 'full', 'partial']
	initial='empty'
	transitions=[
		['toPartial', '*', 'partial', None, ['isEmpty', 'isFull']],
		['toEmpty', '*', 'Empty', 'isEmpty'],
		['toFull', '*', 'Full', 'isFull'],
		]
	
	def __init__(self, capacity=float('inf'), qty=0):
		
		self.capacity=capacity
		self.qty=qty
		self.inputs=set()
		self.outputs=set()
		
		StateMachine.__init__(self, self.states, self.initial, self.transitions)
		
	# --- Conditions
	def isFull(self, event):
		return self.qty>=self.capacity
		
	def isEmpty(self, event):
		return self.qty<=0
	
	# --- Actions
	

class Pipe(StateMachine):
	
	states=['maxRate', 'bottleneck', 'shortage', 'idle']
	initial='idle'
	transitions=[
		['shortage', '*', 'shortage', 'fromEmpty'],
		['bottleneck', '*', 'bottleneck', 'toFull']
		]
	
	def __init__(self, fromContainer, toContainer, maxRate=float('inf')):
		
		self.fromContainer=fromContainer
		self.toContainer=toContainer
		self.maxRate=maxRate
		
		StateMachine.__init__(self, eventController, self.states, self.initial, self.transitions)
		
	# --- Conditions
	
	# --- Actions

def test():
	
	ec=EventController()
	asteroid=Container(capacity=10)
	hold=Container(capacity=5)
	#miner=Pipe(ec, asteroid, hold, 2)
	
	ec.post(Event('tick'))

if __name__== '__main__':
	logging.basicConfig(level=logging.NOTSET)
	logging.info('Running container.py directly.')
	test()
else:
	logging.info('container.py loaded.')
