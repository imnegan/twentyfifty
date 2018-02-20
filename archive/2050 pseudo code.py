print('hello world')

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
		
	def post(self):
		while self.eq:
			e=heappop(self.eq)
			#if e.eventType!='tick': print(e)
			print(e)
			self.lastEventTime=e.eventTime
			for listener in self.listeners:
				listener.notify(e)
				
	def register(self, listener):
		self.listeners.add(listener)
		listener.newEvent(eventType='registered')
		
class Listener:
	def __init__(self, eventManger, name='listener'):
		self.em=eventManger
		self.name=name
		self.em.register(self)
		
	def __repr__(self):
		return self.name
		
	def newEvent(self, eventTime=None, eventType='event', **kwargs):
		if eventTime is None:
			eventTime=self.em.lastEventTime
		event=Event(eventTime, eventType)
		event.originator=self
		for key, value in kwargs.items():
			setattr(event, key, value)
		heappush(self.em.eq, event)
		
	def notify(self, event): pass
	
class Container(Listener):
	def __init__(self, eventManager, capacity=float('inf'), name='container', qty=0):
		Listener.__init__(self, eventManager, name)
		self.capacity=capacity
		self.qty=qty
		
	def deltaQ(self, amount):
		self.qty+=(amount)
		if self.qty==0:
			self.newEvent(eventType='empty')
		elif self.qty==self.capacity:
			self.newEvent(eventType='full')
		
	def space(self):
		return self.capacity-self.qty
		
		
class ContinuousProcess(Listener):
	def __init__(self, eventManager, fromContainer, toContainer, ratio, rate, name='continuous process'):
		Listener.__init__(self, eventManager, name)
		self.fromContainer=fromContainer
		self.toContainer=toContainer
		self.ratio=ratio
		self.rate=rate
		self.prodQ=0.0
		self.state=self.stop
		self.scheduledCompletion=None
		self.lastUpdateTime=None
		
	def start(self): pass
		
	def stop(self): pass
	
	def process(self, updateTime):
		timePassed=updateTime-self.lastUpdateTime
		
		self.lastUpdateTime=updateTime
		
	
	def notify(self, event):
		if self.state==self.process:
			#test production delays
			if event.originator==self.fromContainer and event.eventType=='empty':
				self.newEvent(eventType='production delay')
			elif event.originator==self.toContainer and event.eventType=='full':
				self.newEvent(eventType='production delay')
		elif event.eventType=='queue production' and event.producer==self:
			self.state=go
		
	
		
class Game(Listener):
	def __init__(self, eventManager):
		self.players=[]
		name='game'
		Listener.__init__(self, eventManager, name)
		#post start game event
		heappush(self.em.eq, Event(0.0, 'game start'))
		
		
class SupplyChain(Listener):
	def __init__(self, eventManager):
		name='supply chain'
		Listener.__init__(self, eventManager, name)
		
	def notify(self, event):
		if event.eventType=='req':
			amount=min(event.qty, event.fromContainer.qty, event.toContainer.space())
			event.fromContainer.deltaQ(-amount)
			event.toContainer.deltaQ(amount)
				
		#1st way:
		#1. requisition qty/from/to
		#2. fromContainer says how much it can give
		#3. toContainer says how much it can take
		#4. move min(qty/from/to)
		
class TimeController(Listener):
	def __init__(self, eventManager):
		name='time controller'
		Listener.__init__(self, eventManager, name)
		self.gameTime=0.0
		self.dt=0.5
		self.lastTick=self.gameTime
		
		self.counter=itertools.count()
		self.count=next(self.counter)
		
	def notify(self, event):
		self.gameTime=event.eventTime
		if event.eventType=='game start':
			self.tick()
		if event.eventType=='tick' and self.count<=10:
			self.lastTick=event.eventTime
			self.tick()
			self.count=next(self.counter)
			
	def tick(self):
		_gameTime=self.lastTick+self.dt
		Listener.newEvent(self, _gameTime, 'tick')
		
def main():
	em = EventManager()
	g = Game(em)
	tc=TimeController(em)
	sc=SupplyChain(em)
	
	c1=Container(em, name='c1', qty=20, capacity=100)
	c2=Container(em, name='c2', qty=1, capacity=10)
	
	cp=ContinuousProcess(em, c1, c2, 10, 2)
	
	g.newEvent(eventTime=1.2, eventType='req', fromContainer=c1, toContainer=c2, qty=3)
	em.post()
	
	print(vars(c1))
	print(vars(c2))

if __name__ == "__main__":
	main()
