import logging
import os
import heapq

main_dir = os.path.split(os.path.abspath(__file__))[0]
#data_dir = os.path.join(main_dir, 'data')

#Logging debugging
logging.basicConfig(level=logging.NOTSET)

''' 
logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")


Level			Numeric value
CRITICAL	50
ERROR			40
WARNING		30
INFO			20
DEBUG			10
NOTSET		0
'''

class DefaultObject:
	def __repr__(self):
		repr=str(self.__class__.__name__)
		if hasattr(self, 'name'):
			repr=repr+'{name:'+self.name+'}'
		return repr

class Event(DefaultObject):
	
	def __init__(self, type='event', t=0, **kwargs):
		self.type=type
		self.t=t
		for key, value in kwargs.items():
			setattr(self, key, value)
			
	def __lt__(self, other):
		return self.t < other.t
			
	def __repr__(self):
		return 'Event'+str(self.__dict__)
		
class EventController(DefaultObject):
	
	def __init__(self, name='eventController'):
		self.name=name
		self.members=set()
		self.eventQueue=[]
		heapq.heapify(self.eventQueue)
		
		#self.post(Event(type='EventController.__init__', ec=self))
		
	def register(self, member):
		self.members.add(member)
		self.post(Event(type=member.__class__.__name__+'.__init__', object=member))
		#self.post(Event(type=self.name+'.register', member=member))
		
	def deregister(self, member):
		if member in self.members:
			self.members.remove(member)
		
	def post(self, event):
		#if event has no time then broadcast immediately
		if event.t == 0:
			self.broadcast(event)
		#if event has a scheduled time add event to eventQueue
		elif event.t>0 and event.type!='tick':
			logging.debug('scheduling event:'+str(event))
			heapq.heappush(self.eventQueue, event)
		#2. if event is a tick then iterate through eventQueue where e.t<=tick.t
		elif event.type=='tick':
			if len(self.eventQueue)>0:
				t=self.eventQueue[0].t
				while t<=event.t:
					logging.debug('broadcasting queued event:')
					self.broadcast(heapq.heappop(self.eventQueue))
					if len(self.eventQueue)>0:
						t=self.eventQueue[0].t
					else:
						t=event.t+1
			#broadcast the tick
			self.broadcast(event)
	
	def broadcast(self, event):
		for member in self.members.copy():
			member.onEvent(event)
		if event.type!='tick':
			logging.debug('broadcasting:'+str(event))
			
	def deleteQueuedEvents(self, member):
		self.eventQueue-=member.queuedEvents()
			
class EventControllerMember(DefaultObject):
	
	def __init__(self, eventController):
		self.ec=eventController
		eventController.register(self)
		
	def post(self, event):
		e=event
		e.object=self
		self.ec.post(e)
	
	def queuedEvents(self):
		result=set()
		for event in self.ec.eventQueue:
			if hassattr(event, 'object'):
				if event.object==self:
					result.add(event)
		return result
		
	def onEvent(self, event):
		pass

def test():
	ec=EventController()
	ecm1=EventControllerMember(ec)
	ecm2=EventControllerMember(ec)
	
	ecm1.post(Event('Hello from ecm1'))
	ecm2.post(Event('Hello from ecm2'))
		
if __name__ == "__main__":
	logging.debug('event.py is being run directly')
	test()
else:
	logging.debug('event.py loaded.')
