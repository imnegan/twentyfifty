import heapq, logging

logging.basicConfig(level=logging.NOTSET)

class Event:
	
	def __init__(self, type='event', t=0, **kwargs):
		self.type=type
		self.t=t
		for key, value in kwargs.items():
			setattr(self, key, value)
			
	def __lt__(self, other):
		return self.t < other.t
			
	def __repr__(self):
		return 'Event'+str(self.__dict__)
		
class EventMember:
	
	def __init__(self, eventController):
		self.eventController=eventController
		eventController.register(self)
		
	def post(self, event):
		event.object=self
		self.eventController.post(event)
		
	def onEvent(self, event):
		pass
		
	def deleteEvents(self):
		self.eventController.deleteEvents(self)
		
class EventController:

	def __init__(self):
		self.members=set()
		self.queue=[]
		heapq.heapify(self.queue)
		
	def register(self, member):
		self.members.add(member)
		
	def deregister(self, member):
		if member in self.members:
			self.members.remove(member)
		
	def post(self, event):
		if event.type != 'tick':
			heapq.heappush(self.queue, event)
		else:	#tick event
			while len(self.queue)>0 and self.queue[0].t <= event.t:
				self.broadcast(heapq.heappop(self.queue))
			self.broadcast(event)
				
	def broadcast(self, event):
		logging.debug(event)
		for member in self.members:
			member.onEvent(event)
<<<<<<< HEAD
=======
		if event.type!='tick':
			logging.warning('broadcasting:'+str(event))
			
	def deleteQueuedEvents(self, member):
		self.eventQueue-=member.queuedEvents()
>>>>>>> dcae2121c245eb0a2259371e33c450c81fcf8033
			
	def deleteEvents(self, member):
		for event in self.queue:
			if event.object==member:
				self.queue.remove(event)

def test():
	ec=EventController()
	ecm1=EventMember(ec)
	ecm2=EventMember(ec)
	
	ecm1.post(Event('Hello from ecm1'))
	ecm2.post(Event('Hello from ecm2', t=1))
	
	ec.post(Event(type='tick', t=0))
	ec.post(Event(type='tick', t=1))
	ec.post(Event(type='tick', t=2))

		
if __name__ == "__main__":
	logging.debug('event.py is being run directly')
	test()
else:
	logging.debug('event.py loaded.')
