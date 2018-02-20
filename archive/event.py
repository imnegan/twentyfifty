from heapq import heappush, heappop
import functools

class EventManager:
	def __init__(self):
		self.eq=[] 	#event queue - heapq
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
		#while self.eq:
		e=heappop(self.eq)
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

class Complete(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)
	
class Delivery(Event):
	def __init__(self, toC, amount, **kwargs):
		Event.__init__(self, toC=toC, amount=amount, **kwargs)

class DeltaDt(Event):
	def __init__(self, dt, **kwargs):
		Event.__init__(self, dt=dt, **kwargs)
	
class Empty(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)
	
class EndOfEq(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)
	
class Exit(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)
	
class Full(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)

class Pause(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)

class QProcess(Event):
	def __init__(self, amount, process, **kwargs):
		Event.__init__(self, amount=amount, process=process, **kwargs)

class Register(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)

class Requisition(Event):
	def __init__(self, fromC, toC, amount, check=True, **kwargs):
		Event.__init__(self, fromC=fromC, toC=toC, amount=amount, check=check, **kwargs)

class SoundOff(Event):
	'''Request all listeners to give their status'''
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)

class Start(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)
	
class StartGame(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)
	
class Tick(Event):
	def __init__(self, **kwargs):
		Event.__init__(self, **kwargs)

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
	
class Test:
	one=1

