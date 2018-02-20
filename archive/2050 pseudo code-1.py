'''

class Sat:
	.coe #dict
	.stateVector 
	.
	
	def coeToStateVector(self): pass
	def stateVectorToCoe(self): pass
	def stateVector(self, t): pass
	

class Player:
	.name

'''
from heapq import heappush, heappop 
import functools, itertools

@functools.total_ordering
class Event:
	def __init__(self, eventTime, eventType):
		self.eventTime=eventTime
		self.eventType=eventType

	def __eq__(self, other):
		return self.eventTime == other.eventTime
	
	def __lt__(self, other):
		return self.eventTime < other.eventTime
	
	def __repr__(self):
		return str(vars(self))
	
class EventManager:
	def __init__(self):
		self.eq=[] #heapq
		self.lastEventTime=0.0
		self.listeners=set()
		
	def newEvent(self, eventTime=None, eventType='event', **kwargs):
		if eventTime is None: eventTime=self.lastEventTime
		event=Event(eventTime, eventType)
		for key, value in kwargs.items():
			setattr(event, key, value)
		heappush(self.eq, event)
	
	def post(self):
		while self.eq:
			e=heappop(self.eq)
			if e.eventType!='tick': print(e)
			self.lastEventTime=e.eventTime
			for listener in self.listeners:
			  listener.notify(e)
	
	def register(self, listener):
		self.listeners.add(listener)
		print(listener.name, 'registered as a listener')
		
class Listener:
	def __init__(self, eventManger):
		self.em=eventManger
		self.em.register(self)
		self.name='listener'
		
	def __repr__(self):
	  return self.name
		
	def newEvent(self, eventTime=None, eventType='event', **kwargs):
		if eventTime is None: eventTime=self.em.lastEventTime
		event=Event(eventTime, eventType)
		for key, value in kwargs.items():
			setattr(event, key, value)
		heappush(self.em.eq, event)
		
	def notify(self, event): pass

class Container(Listener):
  def __init__(self, eventManager, capacity=float('inf'), name='container', qty=0):
    self.capacity=capacity
    self.name=name
    self.qty=qty
    
    Listener.__init__(self, eventManager)
  
  def deltaQty(self, amount):
    _qty=self.qty+amount
    if _qty<=0: 
	    self.newEvent(eventType='empty')
	    self.qty=0
	    _deltaQty=amount-_qty
    elif _qty>=self.capacity:
	    self.newEvent(eventType='full')
	    _deltaQty=_qty-self.capacity
	    self.qty=self.capacity
    else:
	    self.qty=_qty
	    _deltaQty=amount
    self.newEvent(eventType='deltaQty', amount=_deltaQty)
    
	    
	   
	  #if not enough left post empty event
	  #if too much post full event
		
class Game:
	def __init__(self):
		self.em=EventManager()
		self.players=[]
		self.tc=TimeController(self.em)
		self.c1=Container(self.em, name='c1', qty=10, capacity=10)
		self.c2=Container(self.em, name='c2', capacity=10)
		
		#post start game event
		self.em.newEvent(0.0, 'game start')
		self.em.post()
		
class Processor(Listener):
	def __init__(self, eventManager):
		self.name='processor'
		Listener.__init__(self, eventManager)
		
class TimeController(Listener):
	def __init__(self, eventManager):
		self.name='time controller'
		self.gameTime=0.0
		self.dt=0.5
		self.lastTick=self.gameTime
		
		self.counter=itertools.count()
		self.count=next(self.counter)
		
		Listener.__init__(self, eventManager)
		
	def notify(self, event):
	  self.gameTime=event.eventTime
	  if event.eventType=='game start':
	    self.tick()
	  if event.eventType=='tick' and self.count<=1000:
	    self.lastTick=event.eventTime
	    self.tick()
	    self.count=next(self.counter)
	      
	def tick(self):
	  _gameTime=self.lastTick+self.dt
	  self.newEvent(_gameTime, 'tick', originator=self) 

g=Game()
