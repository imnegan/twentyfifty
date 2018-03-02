import logging
from transitions import Machine, State

class Miner:
	
	states=['fossicking', 'mining', 'returning', 'unloading', 'idle']
	initial='fossicking'
	transitions=[
		#[name, source, dest, conditions=None, unless=None, before=None, after=None, prepare=None]
		['fuelEmpty', '*', 'idle', 'outOfFuel'],
		['finishUnloading',	'unloading', 'fossicking', 'isEmpty', 'outOfFuel'],
		['readyToMine', 'fossicking', 'mining', 'foundOre', 'outOfFuel'],
		['keepMining', 'mining', 'mining', None, 'isFull', ['mine', 'consumeFuel']],
		['finishMining', 'mining', 'returning', 'isFull', 'outOfFuel'],
		['readyToUnload', 'returning', 'unloading', None, 'outOfFuel'],
		['keepUnloading', 'unloading', 'unloading', None, 'isEmpty', 'unload'],
		]
	
	def __init__(self):
		
		self.fuel=10
		self.capacity=3
		self.qty=0

		self.transitioning=False
		stateDict=[]
		for state in self.states:
			stateDict.append(State(state, on_exit='endTransition'))
		
		self.machine = Machine(model=self, 
			states=stateDict,
			transitions=self.transitions, 
			initial=self.initial,
			auto_transitions=False)
				
		
	def endTransition(self, event):
		self.transitioning=False
			
	def onEvent(self, event):
		self.transitioning=True
		transitions=self.machine.get_triggers(self.state)
		count=0
		while self.transitioning:
			getattr(self, transitions[count])(event)
			count+=1

	# --- Conditions
	def isFull(self, event):
		return self.qty==self.capacity
		
	def isEmpty(self, event):
		return self.qty==0
		
	def outOfFuel(self, event):
		return self.fuel==0
		
	def foundOre(self, event):
		return True
	
	# --- Actions
	def consumeFuel(self, event):
		self.fuel-=1
		logging.warning(self.fuel)
		
	def mine(self, event):
		self.qty+=1
		self.consumeFuel(event)
		
	def unload(self, event):
		self.qty-=1

def test():
	m=Miner()
	while m.state != 'idle':
		m.onEvent(object)
	
if __name__== '__main__':
	logging.basicConfig(level=logging.INFO)
	logging.info('Running miner.py directly.')
	test()
else:
	logging.info('miner.py loaded.')
