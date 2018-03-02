from statemachine import StateMachine
from event import *

class Container(StateMachine):
	
	states=['empty', 'full', 'partial']
	initial='empty'
	transitions=[ #(name, source, dest, conditions=None, unless=None, before=None, after=None, prepare=None)
		['toPartial', '*', 'partial', 'updateMe', ['isEmpty', 'isFull']],
		['toEmpty', '*', 'Empty', 'isEmpty'],
		['toFull', '*', 'Full', 'isFull'],
		]
	
	def __init__(self, capacity=float('inf'), qty=0):
		
		self.capacity=capacity
		self.qty=qty
		self.inputs=set()
		self.outputs=set()
		self.lastupdate=0
		
		StateMachine.__init__(self, self.states, self.initial, self.transitions, prepare_event='prepare')
		
	def dqdt(self):
		_dqdt=0
		for i in self.inputs:
			_dqdt+=i.flowRate()
		for o in self.outputs:
			_dqdt+=i.flowRate()
		
	# --- machine.prepare_event
	def prepare(self, event):
		dt=event.t-self.lastupdate
		if dt<0: dt=0
		self.dty=dt*self.dqdt()
		
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
		
		StateMachine.__init__(self, self.states, self.initial, self.transitions)
		
	def flowrate(self):
		if self.fromContainer.state != 'empty':
			
		
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
