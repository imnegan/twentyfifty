from transitions import Machine
from event import *
import logging

class Game:
	
	states=['idle', 'load', 'play', 'pause', 'save']
	initial=states[0]
	#Transitions (trigger, source, dest, conditions=None, unless=None, before=None, after=None, prepare=None)
	transitions=[
		['startLoading', 'idle', 'load', 'isLoadGameEvent']#, None, None, 'loadGame'],
		#['startPlaying', 'load', 'play', 'isFinishedLoadGameEvent'],
		#['pressPause', 'play', 'pause', ['isPlaying', 'isPlayPauseEvent']],
		#['pressPlay', 'pause', 'play', 'isPlayPauseEvent', 'isPlaying'],
		#['saveGame', 'pause', 'save', 'saveEvent'],
		#['finisedSave', 'save', 'pause', 'finisedSaveEvent']
		]
		
	PLAY, PAUSE = True, False
		
	def __init__(self, name='game'):
		
		self.name=name
		
		self.machine = Machine(model=self, 
			states=Game.states, 
			transitions=Game.transitions, 
			initial=Game.initial,
			auto_transitions=False)
			
	def run(self, event):
		for trigger in self.machine.get_triggers(self.state):
			logging.debug('trigger:', trigger)
			trigger=getattr(self, trigger, self.default)
			trigger(event)
			
	def default(self, *args, **kwargs):
		logging.error('default function')
	
	# ---[conditions functions
	def isLoadGameEvent(self, event):
		logging.debug('isLoadGameEvent... '+str(event.type=='loadGameEvent'))
		if event.type=='loadGameEvent': return True
		else: return False
		
	def isFinishedLoadGameEvent(self, event):
		logging.debug('isFinishedLoadGameEvent')
		if event.type=='finishedLoadGameEvent': return True
		else: return False
		
	
	# ---[before actions functions
	
	# ---[after actions functions
	def loadGame(self, event): #TODO
		logging.debug('***loadGame***')
		#1. load game items (sats etc)
		#2. post finishedLoadGameEvent
		pass
	
	# ---[prepare actions functions
	

g=Game()
logging.debug(g.state)
g.run(event=Event(type='loadGameEvent'))