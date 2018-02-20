from copy import copy
from heapq import heappush, heappop #for EventQueue only
import sys
from collections import Counter

from sceneController import *

class Repr:
	def __repr__(self):
		if hasattr(self, 'name'):
			return self.name+"("+self.__class__.__name__+")"
		else:
			return self.__class__.__name__+str(vars(self))
			
#---Events
class Event(Repr):
	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)
			
class AddResource(Event): pass			#(toC, resource, amount)
class AddResources(Event): pass			#(toC, resources)
class SubtractResources(Event): pass    #(fromC, resources)
class Empty(Event): pass                #(originator)
class Dt(Event): pass					#(dt)
class Full(Event): pass                 #(originator)
class OverflowResources(Event): pass    #(fromC, resources)
class PlayPause(Event): pass            #()
class DQty(Event): pass                 #(originator, amount)
class QEvent(Event): pass                       #(t, event)
class Register(Event): pass                     #(originator)
class Req(Event): pass                          #(fromO, toO, amount)
class SoundOff(Event): pass                     #()
class Stocktake(Event): pass            #(originator)
class Tick(Event): pass                         #(t)

class EventManager:
	def __init__(self):
		self.listeners=[]
		
	def __repr__(self):
		return self.__class__.__name__
		
	def register(self, listener):
		self.listeners.append(listener)
		self.post(Register(originator=listener))
		
	def post(self, event):
		for l in self.listeners:
			l.notify(event)
			
class Listener(Repr):
	def __init__(self, eventManager, **kwargs):
		self.em=eventManager
		self.em.register(self)
		self.name='listener'
		
		for key, value in kwargs.items():
			setattr(self, key, value)
			
	def notify(self, event): pass
	
class TimeController(Listener):
	def __init__(self, eventManager):
		Listener.__init__(self, eventManager)
		self.name='time controller'
		self.t=0.0
		
	def notify(self, event):
		if isinstance(event, Dt):
			self.tick(event.dt)
			
	def tick(self, dt):
		self.t+=dt
		em.post(Tick(t=self.t, dt=dt))
		
class StateMachine:
	def __init__(self):
		self.runState=self.state1
		
	def notify(self, event):
		if isinstance(event, Tick):
			self.runState()
			
	def state1(self):
		if self.condition1():
			self.action1()
			
	def condition1(self): pass
	
	def action1(self):
		self.run=self.state2
		
	def state2(self, event): pass
	
class EventQueue(Listener):
	def __init__(self, eventManager):
		Listener.__init__(self, eventManager)
		self.name='event queue'
		self.eq=[]              #heapq:(time, event)
		
	def queue(self, t, event):
		heappush(self.eq, (t, event))
		
	def notify(self, event):
		if isinstance(event, Tick) and len(self.eq)>0:
			#qe: (t, event)
			qe=copy(heappop(self.eq))
			if event.t>=qe[0]:
				self.em.post(qe[1])
			else:
				heappush(self.eq, qe)
		elif isinstance(event, QEvent):
			self.queue(event.t, event.event)
			
class Debugger(Listener):

	def notify(self, event):
		if not isinstance(event, (Tick, Dt)):
			print('POSTED',event)
		if isinstance(event, SoundOff):
			self.soundOff()
			
	def soundOff(self):
		for l in self.em.listeners:
			print(l)
			
#---Physical objects

class Assembly(Listener):
	def __init__(self, eventManager, name='assembly'):
		Listener.__init__(self, eventManager, name=name)
		self.name=name
		self.components=set()
		
	@property	
	def mass(self):
		m=0
		for c in self.components:
			m+=c.mass
		return m
		
	def notify(self, event):
		if isinstance(event, AddResources) and event.toC==self:
			self.addResources(event.resources)
		elif isinstance(event, SubtractResources) and event.fromC==self:
			self.subtractResources(event.resources)
			
	def addResources(self, resources):
		#also implemented in container
		for r in resources:
			if resources[r]>0:
				for c in self.containers:
					if c.space>0:
						minQ=min(c.space, resources[r])
						_resources=Counter({r:minQ})
						self.em.post(AddResources(toC=c, resources=_resources))
						resources.subtract({r:minQ})
		if sum(resources.values())>0:
			self.em.post(OverflowResources(fromC=self, resources=resources))
	
	def subtractResources(self, resources):
		
		if sum(resources.values())>0:
			self.em.post(ShortageResources(fromC=self, resources=resources))
	
	@property
	def capacity(self):
		_capacity=0
		for c in self.containers:
			_capacity+=c.capacity
		return _capacity
		
		
	@property
	def containers(self):
		_containers=set()
		for c in self.components:
			if isinstance(c, Container):
				_containers.add(c)
			elif isinstance(c, Assembly):
				_containers.union(c.containers)
		return _containers
		
	@property
	def resources(self):
		_resources=Counter()
		for c in self.containers:
			_resources.update(c.resources)
		return _resources
		
	@property
	def space(self):
		_space=0
		for c in self.containers:
			_space+=c.space
		return _space
		
class Component(Listener):
	def __init__(self, eventManager, netMass=0, name='component', **kwargs):
		Listener.__init__(self, eventManager, netMass=netMass, name=name, **kwargs)
		
	def grossMass(self):
		return self.mass
		
class Constants:
	error=1E-10 
	temperatureInSpace=2.7		#deg Kelvin
	G=6.67408E-11 				#m3 kg-1 s-2
	au=149597870700 			#m
	error=1e-10
	
class Container(Component):
	def __init__(self, eventManager, capacity=float('inf'), netMass=0, name='container'):
		Component.__init__(self, eventManager, capacity=capacity, netMass=netMass, name=name)
		self.resources=Counter()
		
	@property	
	def mass(self):
		m=self.netMass
		for r in self.resources:
			m+=r.density#*self.resources[r]
			print(r, self.resources[r])
		
	def notify(self, event):
		if isinstance(event, AddResource) and event.toC==self:
			self.addResource(event.resource, event.amount)
		elif isinstance(event, AddResources) and event.toC==self:
			self.addResources(event.resources)
		elif isinstance(event, SubtractResources) and event.fromC==self:
			self.subtractResources(event.resources)
			
	def addResource(self, resource, amount):
		if amount<=self.space:
			resources=Counter({resource:amount})
		else: 
			resources=Counter({resource:self.space})
			self.em.post(OverflowResources(fromC=self, resources=Counter({resource:amount-self.space})))
		self.resources=self.resources+resources
		self.checkFull()
		
	def checkFull(self):
		if abs(self.space)<Constants.error:
			self.em.post(Full(originator=self))
			
		
	def addResources(self, resources):
		for r in resources:
			self.addResource(r, resources[r])
		self.checkFull()
		
	@property
	def space(self):
		return self.capacity-sum(self.resources.values())

	def subtractResources(self, resources):
		self.resources=self.resources-resources
		for r in self.resources:
			if self.resources[r]==0.0:
				self.em.post(Empty(originator=self, resource=r))
		
class Process(Listener): 
	def nothing(self): pass

class Resource:
	def __init__(self, density=1.0, madeFrom={}, name='resource'):
		self.density=density
		self.madeFrom=madeFrom
		self.name=name
		
	def __repr__(self):
		return self.name
		
class SupplyChain(Listener):
	def notify(self, event):
		if isinstance(event, Req): self.req(event)
		
	def req(self, event):
		amount=min(event.amount, event.fromC.qty, event.toC.space())
		event.fromC.dQty(-amount)
		event.toC.dQty(amount)
		
if __name__ == '__main__':
	em=EventManager()
	tc=TimeController(em)
	eq=EventQueue(em)
	sc=SupplyChain(em)
	
	scene=MyScene2()
	scene.em=em
	em.register(scene)
	scene.tc=tc
	
	d=Debugger(em, name='debugger')
	
	steel=Resource(name='steel')
	ironOre=Resource(name='iron ore')
	
	sh1=Container(em, name='sh1', capacity=20)
	sh2=Container(em, name='sh2', capacity=20)
	
	ioh=Container(em, name='ioh', capacity=20)
	ship=Assembly(em, name='ship')
	ship.components.add(sh1)
	ship.components.add(sh2)
	ship.components.add(ioh)
	em.post(QEvent(t=1, event=Event(name='one')))
	em.post(QEvent(t=2, event=Event(name='two')))
	em.post(QEvent(t=3, event=Event(name='three')))
	
	
	#working
	'''
	
	'''
	
	
	#simulated input:
	print(sh1.resources)
	em.post(AddResources(toC=sh1, resources=Counter({steel:25, ironOre:25})))
	print(sh1.resources)
	'''
	em.post(SoundOff())
	em.post(QEvent(t=1, event=Event(name='one')))
	em.post(QEvent(t=2, event=Event(name='two')))
	em.post(QEvent(t=3, event=Event(name='three')))
	'''
	
	print(sys.platform)
	if sys.platform=='ios':
		run(scene, show_fps=False)
	elif sys.platform=='win32':
		pass

