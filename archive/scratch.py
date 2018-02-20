
class Resource:
	def __init__(self, density=0, name='resource', qty=1):
		self.name=name
		self.density=density
		self.qty=qty
		
	def mass(self):
		return self.density*self.qty
		
steel=Resource(density=10, name='steel', qty=5)

