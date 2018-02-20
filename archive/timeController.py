import itertools, time

from event import Event, Listener, StartGame, Tick, DeltaDt, Exit, 
import twentyfifty



class TimeController(Listener):

	def __init__(self, em):
		self.name='time controller'
		Listener.__init__(self, em, self.name)
		
		self.dt=0.5
		self.nextTick=0.0
		self.ticking=True
		
	def notify(self, event):
		if isinstance(event, (StartGame)): self.run()
		elif isinstance(event, DeltaDt): self.deltaDt(event.dt)
		elif isinstance(event, Exit): self.ticking=False

	def deltaDt(self, dt):
		self.dt=dt
		
	def tick(self):
		if self.ticking:
			self.nextTick+=self.dt
			self.newEvent(Tick(eTime=self.nextTick, dt=self.dt))
