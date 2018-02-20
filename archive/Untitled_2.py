print('hello world')

from heapq import heappush, heappop
import functools, itertools

class EventManager:
	def __init__(self):
		self.eq=[] #heapq
		self.lastETime=0.0
		self.listeners=set()
		self.name='event manager'
	
	def __repr__(self):
		return self.name+': '+str(len(self.eq))+' events'
		
	def newEvent(self, event):
		if event.eTime is None:
			event.eTime=self.lastETime	#instant event
		heappush(self.eq, event)

	def post(self):
		while self.eq:
			e=heappop(self.eq)
			#if e.eventType!='tick': print(e)
			print(e)
			self.lastETime=e.eTime
			for listener in self.listeners:
				listener.notify(e)				

	def register(self, listener):
		self.listeners.add(listener)
		self.newEvent(Register(listener, eTime=1.0))
				
#---Events
@functools.total_ordering
class Event:
	def __init__(self, eTime=None, **kwargs):
		self.eTime=eTime
		for key, value in kwargs.items():
			setattr(self, key, value)
			
	def __eq__(self, other):
		return self.eTime == other.eTime
		
	def __lt__(self, other):
		return self.eTime < other.eTime
		
	def __repr__(self):
		return str(self.__class__.__name__)+str(vars(self))

class Delivery(Event):
	def __init__(self, toC, amount, **kwargs):
		Event.__init__(self, toC=toC, amount=amount, **kwargs)

class Empty(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)
	
class Full(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)

class Register(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)

class Requisition(Event):
	def __init__(self, fromC, amount, **kwargs):
		Event.__init__(self, fromC=fromC, amount=amount, **kwargs)

class SoundOff(Event):
	'''Request all listeners to give their status'''
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)

class Tick(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)

#---Framework classes		
class Listener:
	def __init__(self, em, name='listener'):
		self.name=name
		self.register(em)
		
	def __repr__(self):
		return self.name
		
	def newEvent(self, event):
		event.originator=self
		self.em.newEvent(event)
		
	def register(self, em):
		self.em=em
		self.em.listeners.add(self)
		self.newEvent(Register())
		
	def soundoff(self):
		print(vars(self))
				
	def notify(self, event): pass

class Debugger(Listener):	
	def __init__(self, em, name='debugger'):
		Listener.__init__(self, em, name)
		
	def notify(self, event):
		if isinstance(event, Tick):
			print('len(em.eq): '+len(em.eq))

class Game(Listener):	
	def __init__(self, em, name='game'):
		self.players=[Player(em)]
		Listener.__init__(self, em, name)
		
	def notify(self, event):
		if isinstance(event, SoundOff):
			self.soundoff()
			
	def soundoff(self):
		for listener in self.em.listeners:
			print(vars(listener))

class Player(Listener):	
	def __init__(self, em, name='player'):
		Listener.__init__(self, em, name)
		self.human=False
		self.inventory=set()	#objects under player's control
		
	def addToInventory(self, object):
		self.inventory.add(object)
		
	def removeFromInventory(self, object):
		self.inventory.remove(object)


#---Inventory objects
class Resource:
	def __init__(self, rType, madeFrom=None):
		self.rType=rType 		#eg steel, 
		self.madeFrom=madeFrom	#dict of component resources
		#Other properties:
		#density
		
	def __repr__(self): return self.rType

class InventoryObject(Listener):
	def __init__(self, em, name='inventory object'):
		Listener.__init__(self, em, name)
		
	def scuttle(self, scuttleType=0): 
		#type 1: big badda boom - instant massive energy release
		#type 2: quietly into the night - disable critical systems and purge data. modules are salvageable.
		pass
		
class Container(Listener):
	def __init__(self, em, resource, capacity=float('inf'), name='container', qty=0.0):
		self.resource=resource
		self.capacity=capacity
		self.qty=qty
		#self.name=name
		Listener.__init__(self, em, name)
	
	def fulfillRequisition(self, event):
		if self.qty==0:
			self.newEvent(Empty())
		elif event.amount>self.qty:
			self.newEvent(Delivery(event.originator, self.qty))
			self.qty=0
			self.newEvent(Empty())
		else:
			self.newEvent(Delivery(event.originator, event.amount))
			self.qty-=event.amount

	def delivery(self, event):
		self.qty+=event.amount
	
	def space(self):
		return self.capacity-self.qty
		
	def notify(self, event):
		if isinstance(event, Requisition) and event.fromC==self:
			self.fulfillRequisition(event)
		elif isinstance(event, Delivery) and event.toC==self:
			self.delivery(event)
			
				
'''		
class Process(Listener):
	def __init__(self, em, batchTime, name='process'):
		self.batchTime=batchTime
		Listener.__init__(self, em, name)
		self.inputs={}
		self.outputs={}
		
	def addInputs(self, container, amount):
		self.inputs[container]=amount

	def addOutputs(self, container, amount):
		self.outputs[container]=amount
		
	def limit(self):
		l=1
		for container, amount in self.inputs.items():
			ratio=container.qty/amount
			if ratio<l: l=ratio
		for container, amount in self.outputs.items():
			ratio=container.space()/amount
			if ratio<l: l=ratio
		return l
		
	def process(self):
		l=self.limit()
		for container, amount in self.inputs.items():
			self.em.reqE(self, l*amount, fromC=container)
		for container, amount in self.outputs.items():
			self.em.reqE(self, l*amount, toC=container)
	'''
	
def main():
	em=EventManager()
	l=Listener(em)
	g=Game(em)
	
	ore=Resource('ore')
	energy=Resource('energy')
	steel=Resource('steel', {ore:2, energy:10})
	
	
	sh1=Container(em, steel, qty=1.9, name='steel hopper 1')
	sh2=Container(em, steel, qty=10, name='steel hopper 2')
	
	em.newEvent(SoundOff(eTime=0.1))
	sh2.newEvent(Requisition(sh1, 5, eTime=1.0))
	em.newEvent(SoundOff(eTime=1.1))

	
	em.post()
	
	'''
	p=Process(em, 10)
	p.addInputs(sh1, 2)
	p.addOutputs(sh2, 2)
	
	p.process()
	'''	
	
if __name__ == "__main__":
	main()
