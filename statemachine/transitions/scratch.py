from transitions import Machine
from event import *
import logging

class Game:
	
	states=['idle', 'load', 'play', 'pause', 'save']
	initial=states[0]
	transitions=[
		['startLoading', 'idle', 'load', 'isLoadGameEvent']#, None, None, 'loadGame'],
		]
	
	def __init__(self, name='game'):
		
		self.name=name
		
		self.machine = Machine(model=self, 
			states=Game.states, 
			transitions=Game.transitions, 
			initial=Game.initial,
			auto_transitions=False)

			
g=Game()			