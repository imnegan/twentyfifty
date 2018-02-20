from event import *

class Container(EventControllerMember):
	
	#states
	EMPTY='empty'
	PARTIAL='partial'
	FULL='full'
	
	def __init__(self, eventController, name="container", capacity=float('inf'), qty=0.0):
		
		self.name=name
		self.capacity=capacity
		self.qty=qty
		
		self.inputs=set()
		self.outputs=set()
		
		#Event controller
		EventControllerMember.__init__(self, eventController)

	def space(self):
		return self.capacity-self.qty
		
	def state(self):
		if self.qty==0:
			return Container.EMPTY
		elif self.qty==self.capacity:
			return Container.FULL
		else:
			return Container.PARTIAL
			
	def ioRate(self, inputsOrOutputs):
		'''
		input or output rate
		usage: 
			container.ioRate(container.inputs)
			container.ioRate(container.outputs)
		'''
		rate=0
		for pipe in inputsOrOutputs:
			try:	rate+=pipe.rate()
			except:	pass
		return rate
		
	def fillRate(self):
		return self.ioRate(self.inputs)-self.ioRate(self.outputs)
		
	def timeToFull(self):
		if self.state()==Container.FULL:
			return 0
		elif self.fillRate()<0:
			return float('inf')
		else:
			try: return self.space()/self.fillRate()
			except: return 'div0'
			
	def timeToEmpty(self):
		if self.state()==Container.EMPTY:
			return 0
		elif self.fillRate()>0:
			return float('inf')
		else:
			try: return self.qty/-self.fillRate()
			except: return 'div0'
			
	def recieveEvent(self, event):
		if event.type=='tick':
			self.qty+=self.fillRate()*event.dt
			logging.critical('\n'+str(event.t))
			logging.warning(self)
		
	def __repr__(self):
		return ('\nCONTAINER:'+self.name
			+'\ncapacity:'+str(self.capacity)
			+'\nqty:'+str(self.qty)
			+'\nspace():'+str(self.space())
			+'\nstate():'+str(self.state())
			+'\nself.ioRate(self.inputs):'+str(self.ioRate(self.inputs))
			+'\nself.ioRate(self.outputs):'+str(self.ioRate(self.outputs))
			+'\nfillrate():'+str(self.fillRate())
			+'\ntimeToFull():'+str(self.timeToFull())
			+'\ntimeToEmpty():'+str(self.timeToEmpty()))
			
	
	'''
	def timeToEmpty(self):
		#return self.qty/self.giveRate()
		if self.fillRate()<0:
			return self.qty/self.fillRate()
		else:
			return float('inf')
			'''

			
class Pipe:
	'''
	A pipe sits between two containers and is used to transfer stuff between the two. 
	'''
	def __init__(self, name='pipe', maxRate=0, input=None, output=None):
		self.name=name
		self.maxRate=maxRate
		
		#connect to containers
		self.input=input
		self.output=output
		input.outputs.add(self)
		output.inputs.add(self)
		
	def rate(self):
		'''throughput rate, less than maxRate if there is an input shortage or an upstream bottleneck'''
		#TODO: fix this 
		if self.input.state()!=Container.EMPTY and self.output.state()!=Container.FULL:
			return self.maxRate
		else:
			return 0
		
	def __repr__(self):
		return ('\nPIPE:'+self.name
			+'\nmaxRate:'+str(self.maxRate))
		
def test():
	ec=EventController()

	mine=Container(ec, name='mine', capacity=10, qty=3)
	stockpile=Container(ec, name='stockpile', capacity=15)
	miner=Pipe(name='miner', input=mine, output=stockpile, maxRate=1)

	print(mine)
	print(stockpile)
	print(miner)

	for t in range(1,11):
		ec.post(Event(type='tick', t=t, dt=1))

if __name__ == "__main__":
	#Logging
	import logging
	#logfile = 'debug.log'
	logging.basicConfig(level=logging.NOTSET)
	logging.warning('giveAndTake.py is being run directly')
	test()
else:
	logging.debug('giveAndTake.py loaded.')
