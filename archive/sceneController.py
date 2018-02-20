import time
from twentyfifty import Tick

class MyScene2:
	def __init__(self):
		self.dt=1.0/60
		self.counter=0
		
	def run(self):
		self.tc.tick(self.dt)
			
	def notify(self, event):
		if isinstance(event, Tick):
			self.tc.tick(self.dt)
			time.sleep(self.dt)
			
