import logging
from transitions import Machine, State
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

class StateMachine:
	
	def __init__(self, states, initial, transitions):
		
		self.transitioning=False
		
		stateDict=[]
		for state in states:
			stateDict.append(State(state, on_exit='endTransition'))
		
		self.machine = Machine(model=self, 
			states=stateDict,
			transitions=transitions, 
			initial=initial,
			auto_transitions=False)
		
	def onEvent(self, event):
		self.transitioning=True
		transitions=self.machine.get_triggers(self.state)
		count=0
		while self.transitioning:
			getattr(self, transitions[count])(event)
			count+=1

	def endTransition(self, event):
		self.transitioning=False
	
class Miner(StateMachine, EventMember):
	
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
	
	def __init__(self, eventController):
		
		self.fuel=10
		self.capacity=3
		self.qty=0
		
		StateMachine.__init__(self, self.states, self.initial, self.transitions)
		EventMember.__init__(self, eventController)
	
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
		logging.info(self.qty)
		
	def unload(self, event):
		self.qty-=1

def test():
	ec=EventController()
	m=Miner(ec)
	while m.state != 'idle':
		m.onEvent(object)
	
if __name__== '__main__':
	logging.basicConfig(level=logging.INFO)
	logging.info('Running statemachine.py directly.')
	test()
else:
	logging.info('statemachine.py loaded.')
