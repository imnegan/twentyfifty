from statemachine import StateMachine
from event import *

class Miner(StateMachine):
	
	transitionData=[
		['finishUnloading', 'unloading', 'fossicking', 'isEmpty', 'outOfFuel'],
		['readyToMine', 'fossicking', 'mining', 'foundOre', 'outOfFuel'],
		['keepMining', 'mining', 'mining', None, 'isFull', ['mine', 'consumeFuel']],
		['finishMining', 'mining', 'returning', 'isFull', 'outOfFuel'],
		['readyToUnload', 'returning', 'unloading', None, 'outOfFuel'],
		['keepUnloading', 'unloading', 'unloading', None, 'isEmpty', 'unload'],
		['fuelEmpty', '*', 'idle', 'outOfFuel'],
		]
	
	def __init__(self, eventController):
		
		self.fuel=10
		self.capacity=3
		self.qty=0

		StateMachine.__init__(self, eventController, Miner.transitionData)
		
	# --- Conditions
	def isFull(self, event):
		logging.debug('qty/capacity:'+str(self.qty)+'/'+str(self.capacity))
		return self.qty==self.capacity
		
	def isEmpty(self, event):
		return self.qty==0
		
	def outOfFuel(self, event):
		logging.debug('fuel:'+str(self.fuel))
		return self.fuel==0
		
	def foundOre(self, event):
		return True
	
	# --- Actions
	def consumeFuel(self, event):
		self.fuel-=1
		
	def mine(self, event):
		self.qty+=1
		self.consumeFuel(event)
		
	def unload(self, event):
		self.qty-=1

def test():
	ec=EventController()
	m=Miner(ec)
	print(m.state)
	
	while m.state != 'idle':
		ec.post(Event(type='tick'))
	ec.post(Event(type='tick', tag='final'))

if __name__== '__main__':
	logging.info('Running miner.py directly.')
	test()
else:
	logging.info('miner.py loaded.')
