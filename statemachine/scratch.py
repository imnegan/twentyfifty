class dummy:
	
	def __init__(self):
		self.letter='p'
		
	def a(self):
		print('a'+self.letter)
		
	def b(self):
		print('b')
		
	def c(self):
		print('c')
		
class beta: pass

d=dummy()
b=beta()
b.func=getattr(dummy(), 'a')
b.func()

from csv import DictReader
drobject=[
	['a','b','c'],
	[1,2,3],
	[4,5,6]]
	
output=DictReader(drobject)
print(type(drobject))
#for o in output:
	#print(dict(o))
print(type(drobject)==list())
	

