from stateMachine import *
import logging

def test():
	transitionData=getTransitionsFromCsv('minertransitions.csv')
	m=Miner(transitionData)
	while m.count<5:
		m.run()
	
class Miner(StateMachine):
	
	def __init__(self, transitions):
		StateMachine.__init__(self, transitions)
		
		self.capacity=3
		self.qty=0
		self.count=0
	
	#conditions
	def isEmpty(self):
		return self.qty == 0
	
	def isNotEmpty(self):
		return self.qty>0
	
	def foundOre(self):
		return True
		
	def isNotFull(self):
		return self.qty<self.capacity
		
	def isFull(self):
		return self.qty==self.capacity
		
	def isHome(self):
		return True
		
	def finishedCount(self):
		return self.count==3
		
	#actions
	def mine(self):
		self.qty+=1
		
	def unload(self):
		self.qty-=1
		
	def cycle(self):
		self.count+=1
		
test()


	
