import numpy as np
import orbital
from event import EventControllerMember, Event

class Sat(EventControllerMember):
	def __init__(self, eventController, name='sat', parent=None, mass=0.0, R0=None, V0=None, radius=None):
		self.name=name
		self.parent=parent
		self.children=[]
		self.mass=mass
		self.R0=np.array(R0)
		self.V0=np.array(V0)
		self.radius=radius
		
		#add self to parent
		if parent is not None:
			self.parent=parent
			parent.addSat(self)
	
		#Event controller
		EventControllerMember.__init__(self, eventController)
		
	def addSat(self, sat):
		if sat not in self.children:
			self.children.append(sat)
			self.children.sort(key=lambda x: x.semimajorAxis)
		
	def newParent(self, sat):
		self.parent.children.remove(self)
		self.sat.children.add(self)
		
	def stateVector(self, t):
		try:
			return orbital.rv_from_r0v0(self.R0, self.V0, t, self.mu)
		except:
			print(self, 'stateVector failed at time ', t)
			return([10,10,10],[10,10,10])
	
	@property
	def semimajorAxis(self):
		try:
			return orbital.semimajorAxis(self.R0, self.V0, self.mu)
		except:
			return 0
		
	@property
	def mu(self):
		try:
			return orbital.mu(self.mass, self.parent.mass)
		except:
			return 0
	
	@property
	def period(self):
		a=orbital.semimajorAxis(self.R0, self.V0, self.mu)
		return orbital.periodEllipse(a,self.mu)
	
	@property
	def siblings(self):
		if self.name!='Sun':
			p=self.parent.children
			s={self}
			return p.difference(s)
		else: return set()
	
	'''
	def __repr__(self):
		return str(self.__class__.__name__)+str(self.__dict__)
	'''
					
class AsteroidSpawner(EventControllerMember):
	def __init__(self, eventController, name='Asteroid Spawner'):
		self.name=name
		self.count=0
		
		self.ec=eventController
		eventController.register(self)

	def spawnAsteroid(self, parent):
		self.count+=1
		name='Asteroid '+str(self.count)
		Sat(self.ec, name, parent=parent)
		

if __name__ == "__main__":
    print('sat.py is being run directly')
else:
    print('sat.py loaded.')
