from collections import Counter

class Resource: 

	def __init__(self, name):
		self.name=name
	
	def __repr__(self):
		return self.name

class Container(Counter):

	def __init__(self, capacity=float('inf')):
		self.capacity=capacity
		
	def __hash__(self):
		return id(self)
	
	@property
	def qty(self):
		return sum(self.values())
		
	@property
	def space(self):
		return self.capacity-self.qty
		
class Assembly(list):

	def __hash__(self):
		return id(self)
		
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

	

a=Assembly()
b=Assembly()
c=Container(10)
d=Container(15)
e=Container(30)
f=Container(1)
g=Container(2)

a.append(b)
a.append(c)
a.append(d)

steel=Resource('steel')
iron=Resource('iron')

c[steel]=2
c[iron]=3
d[iron]=10
l=list(a)









