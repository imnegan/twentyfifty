from statemachine import StateMachine
from event import *

class Miner(StateMachine):
	
	transitionData=[
		[unloading, fossicking, [isEmpty, hasFuel]]
		fossicking, mining, [hasFuel, foundOre]
		mining
		returning
		idle
		]
	
	def __init__(self, eventController):
		
		self.fuel=10
		self.capacity=3
		self.qty=0
		
		StateMachine.__init__(self, eventController, Miner.transitionData)
		
	# --- Conditions
	def isFull(self):
		return self.qty==self.capacity
		
	def isEmpty(self):
		return self.qty==0
		
	def hasFuel(self):
		return self.fuel>0
		
	def outOfFuel(self):
		return self.fuel==0
	
	# --- Actions

def test():
	ec=EventController()
	m=Miner(ec)
	
	while m.state != 'idle':
		ec.post(Event(type='tick'))
	ec.post(Event(type='tick', tag='final'))

if __name__== '__main__':
	logging.info('Running miner.py directly.')
	test()
else:
	logging.info('miner.py loaded.')
