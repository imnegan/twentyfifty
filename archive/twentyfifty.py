print('hello world')
from event import *
from timeController import *
from decimal import *
getcontext().prec = 3

class Helper(Listener):
	'''I help move things'''
	def __init__(self, em, name='helper'):
		Listener.__init__(self, em, name)
	
	def notify(self, event):
		if isinstance(event, Requisition):
			if event.check is True:
				self.requisition(event.fromC, event.toC, event.amount)
			else:
				self.requisitionUnchecked(event.fromC, event.toC, event.amount)


	def requisition(self, fromC, toC, amount):
		fromA=fromC.qty/amount
		toA=toC.space()/amount
		a=min(1.0, fromA, toA)	#Availability ratio
		fromC.dQty(-1*a*amount)
		toC.dQty(a*amount)
		
	def requisitionUnchecked(self, fromC, toC, amount):
		fromC.dQty(-amount)
		toC.dQty(amount)
		
class Process(Listener):
	def __init__(self, em, resource, name='process', cycleTime=1):#, wasteRatio=0.5):
		Listener.__init__(self, em, name)
		self.resource=resource		#the resource to be produced
		self.cycleTime=cycleTime	#time to produce 1 unit
		#self.wasteRatio=wasteRatio	#amount of waste [energy] produced
		
		self.inputs={}				#{container: rate}
		self.queue=0.0				#production queue
		self.lastUpdate=None
		self.complete=None			#scheduled event for completion
		self.wip=Resource('WIP')
		self.wipContainer=Container(self.em, self.wip, qty=float('inf'), capacity=float('inf'))
		
	def notify(self, event): 
	#input events: QProcess, Tick, Complete
		processState=self.queue>0 and ((isinstance(event, (QProcess, Complete)) and event.process==self) or isinstance(event, Tick))
		
		if processState:
			self.process(event)
		elif isinstance(event, QProcess) and event.process==self:
			self.qProcess(event)
			
	def qProcess(self, event):
		self.queue+=event.amount
		self.lastUpdate=event.eTime
		
	
	def complete(self, **kwargs): pass
	
	def process(self, event):
		dt=event.eTime-self.lastUpdate
	'''
		print('*****START: ', self.queue)
		fraction=dt/self.cycleTime
		limit=1
		#1. check input limits
		for input, value in self.inputs.items():
			availability=input.qty/value*dt
			if availability<limit: limit=availability
		#2. check output limits
		for output, value in self.outputs.items():
			availability=output.space()/value*dt
			if availability<limit: limit=availability
		#3. transfer using Helper.requisitionUnchecked
		for input, value in self.inputs.items():
			amount=value*limit*fraction
			self.newEvent(Requisition(fromC=input, toC=self.wipContainer, amount=amount, check=False))
		for output, value in self.outputs.items():
			amount=value*limit*fraction
			self.newEvent(Requisition(fromC=self.wipContainer, toC=output, amount=amount, check=False))
		self.queue-=limit*fraction
		print('*****END: ', self.queue)
	'''
		
		
#---Debugger		
class Debugger(Listener):	
	def __init__(self, em, name='debugger'):
		Listener.__init__(self, em, name)
		
	def notify(self, event): pass
			
class Game(Listener):	
	def __init__(self, em, name='game'):
		self.players=[Player(em)]
		Listener.__init__(self, em, name)
		self.playing=False
		
	def Start(self):
		self.newEvent(StartGame())
		self.playing=True
		while self.playing==True:
			self.em.post()
		
	def notify(self, event):
		if isinstance(event, SoundOff):
			self.soundoff()
		elif isinstance(event, Exit):
			self.playing=False
			self.em.post()
			
	def soundoff(self):
		for listener in self.em.listeners:
			print(vars(listener))

class Player(Listener):	
	def __init__(self, em, name='player'):
		Listener.__init__(self, em, name)
		self.human=True
		self.inventory=set()	#objects under player's control
		
	def addToInventory(self, object):
		self.inventory.add(object)
		
	def removeFromInventory(self, object):
		self.inventory.remove(object)
		
	def totalPopulation(self): pass
	def totalMass(self): pass
	def totalAI(self): pass

#---Space objects	
class Sat(Listener):
	def __init__(self, em, mass=0, name='Sat', parent=None, parentName=None):
		self._initParent(parent, parentName)
		
		self.mass=mass
		self.name=name
		self.children=set()
		
		Listener.__init__(self, em, name)
    
	def _initParent(self, parent, parentName):
		self.parent=parent
		if self.parent is not None:
			self.parent.children.add(self)
		elif parentName is not None:
			pass #TODO: Match parentName to parent object
    
	def descendants(self):
		d=self.children
		for child in self.children:
			d=d|child.descendants()
		return d
    
	def position(self, t): pass #TODO
  
	def root(self):
		if self.parent is not None:
			r=self.parent
			while r.parent is not None:
				r=r.parent
			return r
		else: return self
  
	def totalMass(self):
		tm=self.mass
		for child in self.children:
			tm=tm+child.totalMass()
		return tm
    
	def stateVector(self, t): pass
	def coeToStateVector(self, t): pass
	def stateVectorToCoe(self): pass

#---Inventory objects
class Resource:
	'''a singly unit qty in a container'''
	def __init__(self, rType, madeFrom=None, density=1):
		self.rType=rType 		#eg steel,
		self.density=density
		self.madeFrom=madeFrom	#dict of component resources
		#Other properties:
		#density
		
	def __repr__(self): return self.rType

class InventoryObject(Listener):	#Unused
	def __init__(self, em, name='inventory object'):
		Listener.__init__(self, em, name)
		
	def scuttle(self, scuttleType=0): 
		#type 1: big badda boom - instant massive energy release
		#type 2: quietly into the night - disable critical systems and purge data. modules are salvageable.
		pass

#---Components of a structure
class Component:
	def __init__(self, mass=0):
		self.mass=mass
		
	def grossMass(self): 
		return self.mass
			
class Container(Listener, Component):
	def __init__(self, em, resource, capacity=float('inf'), mass=0, name='container', qty=0.0):
		Listener.__init__(self, em, name)
		self.capacity=capacity	#cubic meters TODO: change to volume
		self.mass=mass			#net mass
		self.qty=qty			#cubic meters
		self.resource=resource	#what the container holds
	
	def delivery(self, event):
		self.qty+=event.amount
		
	def dQty(self, amount):
		self.qty+=amount
		if self.qty==0:
			self.newEvent(Empty())
		elif self.space()==0:
			self.newEvent(Full())
	

	def space(self):
		return self.capacity-self.qty
	
	def grossMass(self):
		m=self.mass
		r=self.qty*self.resource.density
		return m+r
		
		
class SuperStructure(Listener, Component):
	'''Made up of Components'''
	def __init__(self, em, name='structure'):
		Listener.__init__(self, em, name)
		self.components=set()
	
	def grossMass(self):
		m=0
		for c in component:
			m+=c.grossMass()
		return m
		
def main():
	#1. programmatic elements
	em=EventManager()
	tc=TimeController(em)
	g=Game(em)
	h=Helper(em)
	d=Debugger(em)
	
	#2. populate objects
	sun=Sat(em, name='Sun', mass=1.989e30)
	
	ironOre=Resource('iron ore')
	energy=Resource('energy')						#Electro-magnetic energy
	steel=Resource('steel', {ironOre:1, energy:10})
	
	space=Container(em, energy, name='grid', qty=float('inf'))

	sh1=Container(em, steel, qty=1.9, name='steel hopper 1')
	sh2=Container(em, steel, qty=10, name='steel hopper 2')
	ironOreHopper=Container(em, ironOre, qty=10, name='iron ore hopper')
	grid=Container(em, energy, qty=100, name='grid')
	
	steelRefinery=Process(em, steel, name='steel refinery', cycleTime=1)
	steelRefinery.inputs={ironOreHopper:1, grid:10}
	
	#3. external inputs:
	d.newEvent(DeltaDt(eTime=6.6, dt=0.1))
	g.newEvent(Exit(eTime=10))


	#4. start the game
	g.Start()
	
	#4.1 working external inputs:
	'''
	d.newEvent(SoundOff(eTime=0.1))
	d.newEvent(Requisition(sh1, sh2, 5, eTime=1.0))
	d.newEvent(SoundOff(eTime=1.1))
	'''
	
	#4.2 known issues:
	
	
	
if __name__ == "__main__":
	main()
	print('...fin')
