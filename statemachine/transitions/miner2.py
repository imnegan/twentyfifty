from transitions import Machine
from gettransitions import getTransitionsFromCsv
import logging

logging.basicConfig(level=logging.NOTSET)

'''
transition notes
****************
Transition__init__(self, source, dest, conditions=None, unless=None, before=None, after=None, prepare=None)

If you need to know which transitions are valid from a certain state, you can use get_triggers:
	m.get_triggers('solid')
	
You can also make a trigger cause a transition from all states to a particular destination by using the '*' wildcard:
	machine.add_transition('to_liquid', '*', 'liquid')
	
A reflexive trigger (trigger that has the same state as source and destination) can easily be added specifying = as destination. This is handy if the same reflexive trigger should be added to multiple states. For example:
	machine.add_transition('touch', ['liquid', 'gas', 'plasma'], '=', after='change_shape')
'''


class Miner:
	
	states=['fossicking', 'mining', 'returning', 'unloading', 'idle']
	transitions=getTransitionsFromCsv('miner2transitions.csv')
	initial=states[0]
	
	def __init__(self, name='miner', capacity=5, qty=0):
		
		self.name=name
		self.capacity=capacity
		self.qty=qty
		self.count=0
		self.runningTransitions=False
		
		self.machine = Machine(model=self, 
			states=Miner.states, 
			transitions=Miner.transitions, 
			initial=Miner.initial,
			auto_transitions=False)
			
		for state in Miner.states:
			on_exit=getattr(self.machine, 'on_exit_'+state)
			on_exit('stopRunningTransitions')
			print('stopRunningTransitions() added to', state)
		
	def run(self):
		self.runningTransitions=True
		while self.runningTransitions:
			print('start state:', self.state)
			for trigger in self.machine.get_triggers(self.state):
				print('trigger:', trigger)
				trigger=getattr(self, trigger)
				trigger()
			print('new state:', self.state)
			print('\n')
	
	# ---[conditions
	def foundOre(self):
		print('foundOre=True')
		return True
		
	def isFull(self):
		print('isFull='+str(self.qty>=self.capacity))
		return self.qty>=self.capacity
		
	def isEmpty(self):
		print('isEmpty='+str(self.qty<=0))
		return self.qty<=0
		
	def isFinished(self):
		print('isFinished='+str(self.count<5))
		return self.count==5
		
	# ---[actions
	def mine(self):
		print('mine')
		self.qty+=1
		
	def unload(self):
		print('unload')
		self.qty-=1
		
	def countCycle(self):
		print('countCycle')
		self.count+=1

	# ---[on_enter/on_exit state functions
	def stopRunningTransitions(self):
		logging.warning('stopRunningTransitions')
		self.runningTransitions=False
		
	# ---[special properties
	'''def __repr__(self):
		d={'state':self.state, 'qty':self.qty, 'capacity':self.capacity, 'count':self.count}
		return self.name+str(d)'''
			
m=Miner()

while m.state!='idle':
	m.run()
	
