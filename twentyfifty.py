import sys
import logging
from event import *
from importsatdata import importSatData
from orbital import *
from sat import *
#from videocontroller import *
from giveAndTake import *

'''
if sys.platform=='win32':
	from IOwin32 import *
elif sys.platform=='ios': 
	from IOios import *
else:print("no video controller loaded")
'''

mainDir=os.path.split(os.path.abspath(__file__))[0]
graphicsDir = os.path.join(mainDir, 'graphics')

#Logging
''' 
logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")

Level		Numeric value
CRITICAL	50
ERROR		40
WARNING		30
INFO		20
DEBUG		10
NOTSET		0
'''

#from physicalmodel import *

def testEvent():
	'''Test event.py functions'''
	e=Event()
	ec=EventController()
	ecm1=EventControllerMember(ec, name='ec1')
	ecm2=EventControllerMember(ec, name='ec2')
	
	ec.post(e)

def testOrbital():
	'''Test orbital.py functions by:
		1. converting a state vector to coe's
		2. converting the coe's back to the sv.'''
		
	mu=398600
	r = np.array([1, 2, 3])
	v = np.array([4, 5, 6])
	deg=pi/180

	coe=coe_from_sv(r, v, mu)
	print(coe)
	print(sv_from_coe(coe, mu))

def testPhysicalmodel():
	'''test physicalmodel.py functions and methods'''
	ec=EventController()
	asteroidSpawner=AsteroidSpawner(ec)
	sun=Sat(ec, 'Sun')
	earth=Sat(ec, 'Earth', parent=sun, xy=(1,1))
	moon=Sat(ec, 'Moon', parent=earth, xy=(0.5, 0.5))
	spaceship=Sat(ec, 'Spaceship', parent=earth)

	asteroidSpawner.spawnAsteroid(sun)
	asteroidSpawner.spawnAsteroid(sun)

def testImportSatData(game):
	for sat in game.sats:
		print(sat.name, sat.children)
		
def testSiblings(game):
	print('++++ testSiblings() ++++')
	for sat in game.sats:
		print(sat,sat.siblings)

def testMu(game):
	print('++++ testMu() ++++')
	for sat in game.sats:
		if sat.name != 'Sun':
			print(sat,sat.mu)

def testStateVector(game):	#TODO fix this!!!
	print('++++ testStateVector() ++++')
	month=365.25*24*60*60/12
	for sat in game.sats:
		if sat.name == 'Earth':
			print(sat, sat.R0, sat.V0, sat.mu)
			for i in range(12):
				r=sat.stateVector((i+1)*month)
				print(r[0])
				
def testSV2(game):
	sat=game.satDict['Earth']
	a=sat.R0
	b=sat.stateVector(0.0)
	print(sat, a)
	for i in range(len(a)):
		print(a[i]-b[0][i])
				
def testSemimajorAxis(game): #DONE
	print('++++ testSemimajorAxis() ++++')
	for sat in game.sats:
		try:
			r=np.linalg.norm(sat.R0)
			ratio=r/sat.semimajorAxis
			print(sat.name, sat.semimajorAxis, ratio)
		except:
			print(sat.name, "NO SEMIMAJOR AXIS")
			
def testPeriod(game): #DONE
	print('++++ testPeriod(game) ++++')
	for sat in game.sats:
		print(sat.name, sat.period, 'seconds', sat.period/60/60/24/365, 'years')

def testChildren(game):
	print('++++ testChildren(game) ++++')
	for sat in game.sats:
		try:
			print(sat, sat.children[-1])
		except:
			print(sat, 'no children')
			
def testCreateSatNameDict(game):
	game.satNameDict={}
	for sat in game.sats:
		game.satNameDict[sat.name]=sat
	print(game.satNameDict)
	
def testSatImgFile(sat):
	print(satImgFile(sat))
	
def testKepler_U():
	r0  = 10000
	vr0 = 3.0752
	dt  = 3600
	a   = -19655
	
	alpha = 1/a
	mu=398600
	print('kepler_U:', kepler_U(dt, r0, vr0, alpha, mu))
	print('correct answer: 128.511')
	
def testContainer(ec):
	c=Container(ec)
		
class Game(EventControllerMember):

	def __init__(self, eventController, name='game'):
			
		self.name=name
		
		#Event controller
		EventControllerMember.__init__(self, eventController)
		#self.post(Event(type='Game.__init__', game=self))
		
		#Import sat data
		self.post(Event(type='importSatData', status='start'))		
		self.sats=importSatData(eventController)
		self.satDict=dict()
		for sat in self.sats:
			self.satDict[sat.name]=sat
		self.post(Event(type='importSatData', status='complete'))
		
		#start the game
		logging.warning('startTheGame')
		self.post(Event(type='startTheGame'))
				
if __name__ == "__main__":
	logging.warning('twentyfifty.py is being run directly')
	logging.info(sys.platform)
	
	#load controllers
	ec=EventController()
	#vc=VideoController(ec)
	game=Game(ec)

	#test things
	testContainer(ec)
	
	
else:
	print('twentyfifty.py loaded.')	
	


