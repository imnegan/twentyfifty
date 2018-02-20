from scene import *
import numpy as np
from event import EventControllerMember, Event

import sound
import random
import math
import os
A = Action

mainDir=os.path.split(os.path.abspath(__file__))[0]
graphicsDir = os.path.join(mainDir, 'graphics')

'''
class MyScene (Scene):
	def setup(self):
		pass
		
	def did_change_size(self):
		pass
		
	def update(self):
		pass
		
	def touch_began(self, touch):
		pass
		
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass
'''

class SystemScene(Scene):
	
	def __init__(self, eventController, system, name='systemScene'):
		
		self.name=name
		self.system=system
		
		#scalePosition: scaleLog or scale
		self.scalePosition=scale
		
		#add SatSprite to each sat
		#INFO:Now done by vc
		'''
		for sat in game.sats:
			sat.sprite = SatSprite(satImgFile(sat))
		'''
		
		#Event controller
		self.ec=eventController	
		self.ec.post(Event(type='VideoController.__init__', vc=self))		
		eventController.register(self)
		
		#run scene
		Scene.__init__(self)
		run(self, show_fps=True, orientation=LANDSCAPE)
		
		#display system sprites
		self.displaySystemSprites()
		
	def displaySystemSprites(self):
		#add system sprites
		self.system.sprite.position=self.size/2
		self.system.sprite.size=20,20
		self.add_child(self.system.sprite)
		
		#add children sprites
		for sat in self.system.children:
			sat.sprite.size=20,20
			self.system.sprite.add_child(sat.sprite)
		
	def update(self): 
		#TODO: update positions
		for sat in self.system.children:
			sat.sprite.position=np.array(self.scalePosition(sat, self.t*10e6))*np.array(self.size/2)
		
class SatSprite(SpriteNode):
	def __init__(self, sat):
		print('Loading sat.sprite:', sat)
		SpriteNode.__init__(self, satImgFile(sat))


'''
class SystemSprite(SatSprite):
	
	def __init__(self, sat, parentNode):
		
		#add main sat
		if len(sat.children) == 0:
			sat.sprite.size = parentNode.size/2
		else:
			sat.sprite.size = 20,20
		sat.sprite.position = parentNode.size/2
		
		parentNode.add_child(sat.sprite)
		
		#add child sats
		for s in sat.children:
			print('trying to add:', s)
			sat.sprite.add_child(s.sprite)
			
			#Position child sprite
			s.sprite.position = np.array(logScale(s, 0))*np.array(parentNode.size/2)
			
			#TODO: Size 
			s.sprite.size=(20,20)
'''
			
def logScale(sat, t):
	parent=sat.parent
	
	minSemimajor=parent.children[0].semimajorAxis
	maxSemimajor=parent.children[-1].semimajorAxis
	
	minLog=np.floor(np.log10(minSemimajor))
	maxLog=np.ceil(np.log10(maxSemimajor))-minLog
	
	xInput=sat.stateVector(t)[0][0]
	if xInput<0: 
		xSign=-1
		xInput=-xInput
	else:
		xSign=1
	xLog=np.log10(xInput)-minLog
	xOutput=xSign*(xLog)/maxLog
	
	yInput=sat.stateVector(t)[0][1]
	if yInput<0: 
		ySign=-1
		yInput=-yInput
	else:
		ySign=1
	yLog=np.log10(yInput)-minLog
	yOutput=ySign*(yLog)/maxLog
	
	return xOutput, yOutput
	
def scale(sat, t):
	parent=sat.parent
	
	minSemimajor=parent.children[0].semimajorAxis
	maxSemimajor=parent.children[-1].semimajorAxis
	
	maxScale=maxSemimajor*1.1
	
	xInput=sat.stateVector(t)[0][0]
	yInput=sat.stateVector(t)[0][1]
	
	xOutput=xInput/maxScale
	yOutput=yInput/maxScale
	
	return xOutput, yOutput

	
		
def satImgFile(sat):
	return graphicsDir+'/'+sat.name+'.jpg'
		
if __name__ == "__main__":
	print('IOios.py is being run directly')
else:
	print('IOios.py loaded.')

