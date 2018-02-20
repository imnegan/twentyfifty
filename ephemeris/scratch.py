import callhorizons, csv

class Sat(callhorizons.query):
	def __init__(self, targetNumber, smallbody=False):
		callhorizons.query.__init__(self, targetNumber, smallbody=smallbody)
		self.set_discreteepochs('2469807.5')
		self.get_ephemerides(568)
		
s=Sat('034')
print(s.data['targetname'])
