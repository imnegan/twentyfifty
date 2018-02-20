from scene import *
import sound
import random
import math
A = Action

from event import *
import numpy as np

mainDir=os.path.split(os.path.abspath(__file__))[0]
graphicsDir = os.path.join(mainDir, 'graphics')



class VideoController(EventControllerMember):
	'''
	event sat.__init__:
		1. create a systemSprite and satSprite objects attached to sat
		2. event.sat.parent.systemSprite.add_child(satSprite)
		
	'''
	def __init__(self, eventController):
		
		#Event controller
		EventControllerMember.__init__(self, eventController)
		
		self.scale=logScale
		self.mainBackground=MainBackground(eventController, self)
		self.post(Event(
				type = 'MainBackground.__init__', 
				scene = self.mainBackground))
		self.mainSystem=None #the central sat onscreen
		
	def recieveEvent(self, event):
		
		if event.type=='startTheGame':
			print(timeScale(self.mainSystem))
			run(self.mainBackground,
				show_fps=True,
				orientation=LANDSCAPE)
				
		if event.type=='Sat.__init__':
			sat=event.object
			
			#systemSprite
			sat.systemSprite=SystemSprite(sat, (100,100))
			self.post(Event(
				type = 'SystemSprite.__init__', 
				systemSprite = sat.systemSprite))
			
			#satSprite
			sat.satSprite=SatSprite(sat)
			self.post(Event(
				type = 'SatSprite.__init__', 
				satSprite = sat.satSprite))
				
			#add satSprite to sat.parent.systemSprite
			if sat.name != 'Sun':
				sat.parent.systemSprite.add_child(sat.satSprite)

			
			#make the sun the main system and add to bacground scene
			else:
				self.mainSystem=sat
				self.mainBackground.add_child(self.mainSystem.systemSprite)
				
		if event.type=='tick':
			
			#update mainSystem size and recenter
			self.mainSystem.systemSprite.position= self.mainBackground.size/2
			self.mainSystem.systemSprite.size= self.mainBackground.size
			
			
			#recenter mainsystem mainsprite
			self.mainSystem.systemSprite.mainSatSprite.position= 0,0
			
			#update child sat position
			for sat in self.mainSystem.children:
				sat.satSprite.position=self.scale(sat, event.t)*sat.satSprite.parent.size/2

class MainBackground(Scene):

	def __init__(self, eventController, videoController):

		Scene.__init__(self)
		self.vc=videoController
		
		#Event controller
		EventControllerMember.__init__(self, eventController)
		
	def setup(self):
		self.background_color='black'
		
	def update(self):
		self.post(Event(type='tick',
			t=self.t*timeScale(self.vc.mainSystem), dt=self.dt))

class SystemSprite(Node): 
	'''
	created when a sat is initialised 
	init vars: sat, size
	includes: 
		1. a tranparent rect of input size
		2. the sat image at the centre of the rect
		3. child satSprite objects that orbit
		
	def update(self, time):
		1. sat image position=center(self)
		2. update sat.children positions
	'''
	def __init__(self, sat, size):
		Node.__init__(self)
		self.mainSatSprite=SatSprite(sat)
		self.add_child(self.mainSatSprite)
		self.size=size
	
class SatSprite(SpriteNode):
	def __init__(self, sat):
		SpriteNode.__init__(self, satImgFile(sat))
		self.size=10,10
	
def center(rect):
	'''
	return center of rect
	'''
	return rect.size/2

def logScale(sat, t):
	parent=sat.parent
	
	minA=parent.children[0].semimajorAxis
	maxA=parent.children[-1].semimajorAxis
	
	minLog=np.floor(np.log10(minA))
	maxLog=np.ceil(np.log10(maxA))
	
	xy=sat.stateVector(t)[0][0:2]
	
	satR=np.linalg.norm(xy)
	satLog=np.log10(satR)
	
	scaledR=(satLog-minLog)/(maxLog-minLog)
	
	xyScaled=(scaledR/satR)*xy
	
	return xyScaled
	
def linearScale(sat, t):
	parent=sat.parent
	
	#minSemimajor=parent.children[0].semimajorAxis
	maxSemimajor=parent.children[-1].semimajorAxis
	
	maxScale=maxSemimajor*1.1
	
	xInput=sat.stateVector(t)[0][0]
	yInput=sat.stateVector(t)[0][1]
	
	xOutput=xInput/maxScale
	yOutput=yInput/maxScale
	
	return xOutput, yOutput
		
def satImgFile(sat):
	return graphicsDir+'/'+sat.name+'.jpg'
	
def timeScale(system):
	return system.children[0].period/5
	
