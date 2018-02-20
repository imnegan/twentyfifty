class ProcessIOContainer:
	def __init__(self, container, amount, processIOtype='input'):
		self.container=container
		self.amount=amount					#qty consumed/produced each second
		self.processIOtype=processIOtype	#'input'/'output'/'waste'
			
class Process(Listener):
	def __init__(self, eventManager, processIOcontainers, rate, name='process'):
		Listener.__init__(self, eventManager, name)
		self.processIOcontainers=processIOcontainers #list with containers and amounts
		self.rate=rate			#number of seconds to produce output
		self.prodQ=0.0			#production queue, amount of output to produce
		self.state=self.stop
		self.lastUpdateTime=None
		
	def checkAvailability(self):
		availPct=1.0
		for c in self.processIOcontainers:
			if c.processIOtype=='input':
				avail=c.container.qty/(c.amount/self.rate)
			elif c.processIOtype=='output':
				avail=c.container.space()/(c.amount/self.rate)
			if avail<availPct: availPct=avail
		return availPct
			
	def start(self, eventTime):
		#1. Calculate scheduled completion and schedule event
		completionTime=eventTime+self.rate
		self.newEvent(eventTime=eventTime, eventType='start')
		self.newEvent(eventTime=completionTime, eventType='scheduled completion')
		#2. Change state to process
		self.state=self.process
		
	def stop(self, eventTime): 
		self.newEvent(eventTime=eventTime, eventType='stop')
	
	def pause(self, eventTime): 
		self.newEvent(eventTime=eventTime, eventType='pause')

	def process(self, eventTime):
		self.newEvent(eventTime=eventTime, eventType='process')
		availPct=self.checkAvailability()
		if availPct==0:
			self.state=self.pause
			return
			
		timePassed=eventTime-self.lastUpdateTime
		self.lastUpdateTime=eventTime
		ableToProducePercents=[]
		#for each input: 

	def notify(self, event):
		#start
		#process
		if self.state==self.process:
			if event.eventType=='tick':
				self.state(event.eventTime)
			elif event.eventType=='scheduled completion' and event.originator==self:
				self.state(event.eventTime)
		#stop
		
class SupplyChain(Listener):
	def __init__(self, eventManager):
		name='supply chain'
		Listener.__init__(self, eventManager, name)
		
	def notify(self, event):
		if event.eventType=='req':
			amount=min(event.qty, event.fromContainer.qty, event.toContainer.space())
			event.fromContainer.deltaQ(-amount)
			event.toContainer.deltaQ(amount)
			
	def reqEvent(self, fromContainer, toContainer, qty, eventTime=None):
		if eventTime is not None:
			self.newEvent(eventTime=eventTime, eventType='req', 
				fromContainer=fromContainer, toContainer=toContainer, qty=qty)
		else: 
			self.newEvent(eventType='req', fromContainer=fromContainer, 
			toContainer=toContainer, qty=qty)

pIOcs=[ProcessIOContainer(ore, 5, 'input'), 
	ProcessIOContainer(energy, 10, 'input'),
	ProcessIOContainer(steel, 1, 'output'),
	ProcessIOContainer(energy, 100, 'output')]
	
p=Process(em, pIOcs, 3, name='process')
p.checkAvailability()
p.start(0.1)

