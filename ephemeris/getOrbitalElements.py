import callhorizons, csv
'''
saturn = callhorizons.query('699', smallbody=False)
saturn.set_discreteepochs('2469807.5')
saturn.get_elements()
'''

class Sat(callhorizons.query):
	def __init__(self, targetNumber, smallbody=False):
		callhorizons.query.__init__(self, targetNumber, smallbody=smallbody)
		self.set_discreteepochs('2469807.5')
		self.get_elements()
		
		#name
		s=str(self.data['targetname'])
		self.name=s[2:s.index('(')-1]

'''
		   +------------------+-----------------------------------------------+
           | Property         | Definition                                    |
           +==================+===============================================+
           | targetname       | official number, name, designation [string]   |
           +------------------+-----------------------------------------------+
           | H                | absolute magnitude in V band (float, mag)     |
           +------------------+-----------------------------------------------+
           | G                | photometric slope parameter (float)           |
           +------------------+-----------------------------------------------+
           | datetime_jd      | epoch Julian Date (float)                     |
           +------------------+-----------------------------------------------+
           | e                | eccentricity (float)                          |
           +------------------+-----------------------------------------------+
           | p                | periapsis distance (float, au)                |
           +------------------+-----------------------------------------------+
           | a                | semi-major axis (float, au)                   |
           +------------------+-----------------------------------------------+
           | incl             | inclination (float, deg)                      |
           +------------------+-----------------------------------------------+
           | node             | longitude of Asc. Node (float, deg)           |
           +------------------+-----------------------------------------------+
           | argper           | argument of the perifocus (float, deg)        |
           +------------------+-----------------------------------------------+
           | Tp               | time of periapsis (float, Julian Date)        |
           +------------------+-----------------------------------------------+
           | meananomaly      | mean anomaly (float, deg)                     |
           +------------------+-----------------------------------------------+
           | trueanomaly      | true anomaly (float, deg)                     |
           +------------------+-----------------------------------------------+
           | period           | orbital period (float, Earth yr)              |
           +------------------+-----------------------------------------------+
           | Q                | apoapsis distance (float, au)                 |
           +------------------+-----------------------------------------------+
'''
		
planet_indices=range(199, 1000, 100)
planets=[]

for i in planet_indices:
	planets.append(Sat(i))
	
fields=['targetname', 'a', 'e', 'p', 'incl', 'node', 'argper', 'Tp', 'meananomaly', 'trueanomaly', 'period', 'Q']

rows=[]
for p in planets:
	row=[]
	for f in fields:
		if f=='targetname':
			s=str(p.data['targetname'])
			name=s[2:s.index('(')-1]
			row.append(name)
		else:
			row.append(float(p.data[f]))
	rows.append(row)
	
fields[0]='name'

f = open('orbitalElements.csv', 'w')
writer = csv.writer(f, delimiter=',', lineterminator='\n')
writer.writerow(fields)
writer.writerows(rows)
f.close()

exit()



