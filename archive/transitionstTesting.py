from transitions import Machine
from random import random
from collections import defaultdict
import csv


class Process:
	states = ['idle', 'ready', 'process']
	transitions = [
		['queueIsGreaterThanZero', 'idle', 'ready'],
		['inputsOK', 'ready', 'process'],
		['stockOut', 'process', 'ready'],
		['queueIsGreaterThanZero', 'process', 'process'],# after='reduceQueue'],
		['queueIsZero', 'process', 'idle'],
		['pause', '*', 'idle']
	]
	
	
	def __init__(self, name='process'):
		self.name=name
		self.queue=0
		
		
		self.machine=Machine(model=self, states=self.states, transitions=self.transitions, initial='idle')
		
	def reduceQueue(self):
		self.queue-=1

class Miner:
	def __init__(self, name='miner'):
		self.states=['searching', 'going', 'mining', 'returning', 'unloading', 'idle']
		
		self.transitionFields=['trigger', 'source', 'dest', 'conditions', 'before', 'after', 'prepare']
		
		self.transitionList=[
			['foundTarget', 'searching', 'going', 'randomCondition'],
			['arrived', 'going', 'mining'],
			['notFinishedMining', 'mining', '='],
			['finishedMining', 'mining', 'returning'],
			['arrived', 'returning', 'unloading'],
			['holdEmpty', 'unloading', 'searching'],
			['pause', '*', 'idle'],
			['unpauseSearching', 'idle', 'searching'],
			['unpauseGoing', 'idle', 'going'],
			['unpauseMining', 'idle', 'mining'],
			['unpauseReturning', 'idle', 'returning'],
			['unpauseUnloading', 'idle', 'unloading']
		]
		
		self.transitions=[]
		for t in self.transitionList:
			self.transitions.append(dict(zip(self.transitionFields, t)))
	
		self.name=name
		self.queue=0
		
		self.machine=Machine(
			model				= self, 
			states				= self.states, 
			initial				= 'searching', 
			transitions			= self.transitions, 
			auto_transitions	= False)
			
		self.mapTransitionsToStates()
		
	def randomCondition(self):
		test = random()
		print(test)
		return test > 0.5
		
	def run(self):
		trigger=partial(self.STMap[self.state][0])
		
	def __repr__(self):
		return self.name+':'+str(self.state)
		
	def returnState(self):
		return self
		
	def mapTransitionsToStates(self):
		self.STMap={k:[] for k in self.states}
		for t in self.transitions:
			if t['source'] in self.states:
				self.STMap[t['source']].append(t['trigger'])
			elif t['source']!='*':
				self.states.append(t['source'])
				self.STMap[t['source']].append(t['trigger'])
		for t in self.transitions:
			if t['source']=='*':
				for s in self.states:
					self.STMap[s].append(t['trigger'])
				
			
		
		
		
		
p=Process()
m=Miner()

for s in m.STMap:
	print(s, m.STMap[s])

print('fin') 