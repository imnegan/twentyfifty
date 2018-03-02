from statemachine import StateMachine
from event import *

class Container(StateMachine, EventMember):
	
	states=['empty', 'full', 'stable', 'emptying', 'filling']
	initial='empty'
	transitions=[ #(name, source, dest, conditions=None, unless=None, before=None, after=None, prepare=None)
		['beStable','*','stable','isStable'],
		['startFilling',['empty', 'stable'],'filling','isFilling','isFull'],
		['startEmptying',['full', 'stable'],'emptying','isEmptying','isEmpty'],
		['stopFilling','filling','full',['isFull', 'isFilling'], None, None, 'fullCorrection'],
		['stopEmptying','emptying','empty',['isEmpty', 'isEmptying'], None, None, 'emptyCorrection']
		]
	
	def __init__(self, eventController, capacity=float('inf'), qty=0):
		
		self.capacity=capacity
		self.qty=qty
		self.inputs=set()
		self.outputs=set()
		self.lastupdate=0
		
		StateMachine.__init__(self, self.states, self.initial, self.transitions, prepare_event='prepare')
		EventMember.__init__(self, eventController)
		
	def addPipe(self, type, pipe):
		self.getattr(self, type).add(pipe)
		
	def removePipe(self, type, pipe):
		self.getattr(self, type).remove(pipe)
		
	def dqdt(self):
		_dqdt=0
		for i in self.inputs:
			_dqdt+=i.flowRate()
		for o in self.outputs:
			_dqdt+=i.flowRate()
		logging.debug('dqdt='+str(_dqdt))
		return _dqdt
		
	def space(self):
		return self.capacity-self.qty
		
	def timeToFull(self):
		if self.isFilling() and not self.isFull():
			return self.space()/self.dqdt
			
	def timeToEmpty(self):
		if self.isEmptying and not self.isEmptying:
			return self.qty/self.dqdt
		
	# --- machine.prepare_event
	def prepare(self, event):
		dt=event.t-self.lastupdate
		if dt<0: dt=0
		self.dt=dt*self.dqdt()
		
	# --- Conditions
	def isFull(self, event):
		return self.qty>=self.capacity
		
	def isEmpty(self, event):
		return self.qty<=0
		
	def isFilling(self, event):
		return self.dqdt()>0
		
	def isEmptying(self, event):
		return self.dqdt()<0
		
	def isStable(self, event):
		return self.dqdt()==0
	
	# --- Actions
	def fullCorrection(self, event):
		if self.qty>self.capacity:
			logging.error('overcapacity, correcting..')
			self.qty=self.capacity
			
	def emptyCorrection(self, event):
		if self.qty<0:
			logging.error('negative qty, correcting..')
			self.qty=0
	

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
		if self.fromContainer.state != 'empty': pass
			
		
	# --- Conditions
	
	# --- Actions

def test():
	
	ec=EventController()
	asteroid=Container(ec, capacity=10)
	hold=Container(ec, capacity=5)
	#miner=Pipe(ec, asteroid, hold, 2)
	
	ec.post(Event('tick'))

if __name__== '__main__':
	logging.basicConfig(level=logging.NOTSET)
	logging.info('Running container.py directly.')
	test()
else:
	logging.info('container.py loaded.')
