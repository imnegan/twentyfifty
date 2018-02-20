from collections import Counter	
		
class Resource: 

	def __init__(self, name='resource', density=1.0):
		self.name=name
		self.density=density
	
	def __repr__(self):
		return self.name

		
class Package(Counter):
	"""
	The Package class is a Counter object used when transferring resources between containers.
	"""

	def __mul__(self, scalar):
		"""multiply the quantities of resources by a scalar"""
		_result=Package()
		for c in self:
			_result[c]=self[c]*scalar
		return _result	
	
	def __imul__(self, scalar):
		"""multiply the quantities of resources by a scalar and update results"""
		for c in self:
			self[c]*=scalar
		return self
		
	@property
	def mass(self):
		m=0
		for r in self.items():
			m+=r[0].density*r[1]
		return m
		
	@property
	def qty(self):
		return sum(self.values())

	
class Container(Package):

	def __init__(self, capacity=float('inf'), name='container'):
		self.capacity=capacity
		self.name=name
		self.contents=self
	
	def __hash__(self):
		'''to give the class a unique id to enable it to be part of an assembly set'''
		return id(self)
		
	def recieve(self, package):
		"""
		Reciprical of the send() method.
		Continuous ie fractional recieving process. 
		Returns a note to the sender how much has been accepted based on space available.
		"""
		if self.space==0:
			return package
		else:
			acceptedPackage=package*min(self.space/package.qty, 1)
			self+=acceptedPackage
		return acceptedPackage
			
	def send(self, package, target):
		'''
		Reciprical of the receive() method.
		'''
		self-=target.recieve(package)
		
	def transferPackage(self, package, fromC, toC):
		#1: check how much is available in fromC
		for r in package:
			qty=min(package[r], fromC[r]) # TODO
			package[r]=qty
		#2: check space avail
		factor=min(toC.space/package.qty, 1)
		package*=factor
		#3: make transfer
		fromC-=package
		toC+=package 
		
	@property
	def space(self):
		return self.capacity-self.qty

	
class Assembly(set):
	
	def __hash__(self):
		return id(self)
	
	# TODO:
	def __iadd__(self, other): pass
	def __imul__(self, scalar): pass
		
	@property
	def capacity(self):
		cap=0
		for c in self:
			cap+=c.capacity
		return cap
		
	@property
	def containers(self):
		_containers=set()
		for component in self:
			if isinstance(component, Container):
				_containers.add(component)
			elif isinstance(component, Assembly):
				_containers=_containers|component.containers
		return _containers
		
	@property
	def contents(self):
		_contents=Container()
		for c in self:
			_contents+=c.contents
		return _contents

	@property
	def mass(self):
		m=0
		for c in self:
			m+=c.mass
		return m
		
	@property
	def qty(self):
		q=0
		for c in self:
			q+=c.qty
		return q
			
	@property
	def space(self):
		s=0
		for c in self:
			s+=c.space
		return s
		
# TODO
class Component:
	"""
	The Component class is a fundamental building block for ships, sats, bases and other natural structures.
	It defines some of the physical properties such as mass, strength, and reflectivity.
	The component class is not intended to perform actions, instead it should be compined with other classes such as container or drive.
	"""
	pass
		
#************************************
steel=Resource('steel', 10)
ore=Resource('ore', 5)
gold=Resource('gold', 20)

b=Container(name='b', capacity=30)
b[steel]=20
b[ore]=10

c=Container(capacity=40, name='c')
c[steel]=20
c[ore]=10

d=Container(30)
d[steel]=20
print('d', d.mass)

a=Assembly()
a.add(b)
a.add(c)
a.add(d)

f=Container(10)
f[steel]=1
g=Container(10)
g[steel]=2

h=Assembly()
h.add(f)
h.add(g)
h.add(a)

p=Package()
p[gold]=20

p1=Package()
p1[steel]=20

print('h.containers', h.containers)
print('a.contents', a.contents)
print('b.contents', b.contents)
print('c.contents', c.contents)
print('d.contents', d.contents)
print('f.contents', f.contents)
print('g.contents', g.contents)
print('h.contents', h.contents)

b.transferPackage(p1, b, c)

print('test differences')

print('fin')