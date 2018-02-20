import csv, os
from collections import defaultdict

from sat import Sat
from event import *

'''
Horizons https://ssd.jpl.nasa.gov/horizons.cgi

Example settings:

Ephemeris Type [change] :       VECTORS
Target Body [change] :  Earth [Geocenter] [399]
Coordinate Origin [change] :    Solar System Barycenter (SSB) [500@0]
Time Span [change] :    discrete time(s)=2050-01-01 00:00
Table Settings [change] :       output units=KM-S; CSV format=YES
Display/Output [change] :       plain text

Ephemeris Type [change] :       VECTORS
Target Body [change] :  Europa (JII) [502]
Coordinate Origin [change] :    Jupiter (body center) [500@599]
Time Span [change] :    discrete time(s)=2050-01-01 00:00
Table Settings [change] :       output units=KM-S; CSV format=YES
Display/Output [change] :       plain text

'''



def importSatData(ec):

	'''#file location info https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script
	__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__)))
	csvfile = open(os.path.join(__location__, 'satdata.csv'))
	'''
	
	ec.post(Event(type='importSatData', status='start'))		
	
	#file location from pygame 'Chimp' example
	main_dir = os.path.split(os.path.abspath(__file__))[0]
	#data_dir = os.path.join(main_dir, 'data')
	csvfile = open(os.path.join(main_dir, 'satdata.csv'))

	
	reader = csv.DictReader(csvfile)
	
	sats=set()
	
	for row in reader:
		if len(sats)>0:
			for sat in sats:
				if sat.name==row['parent']:
					parent=sat
					break
		else: parent=None
		R0=(float(row['rx0'])*1000,float(row['ry0'])*1000,float(row['rz0'])*1000)
		V0=(float(row['vx0'])*1000,float(row['vy0'])*1000,float(row['vz0'])*1000)
		sats.add(Sat(ec, row['name'], parent, float(row['mass']), R0, V0))
	'''for sat in sats:
	if sat.name=='Sun':
	print(sat.name, sat.mass)
	else:
	print(sat.name, sat.parent.name, sat.mass)'''
	return sats
	
if __name__ == "__main__":
	print('importsatdata.py is being run directly')
else:
	print('importsatdata.py loaded.')
	
'''
ec=EventController()
sats=main(ec)
for sat in sats:
	print(sat.name, sat.R0, sat.V0)
'''

