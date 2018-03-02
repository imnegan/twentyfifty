from statemachine import StateMachine
import logging
logging.basicConfig(level=logging.NOTSET)

states=['one', 'two', 'three']
initial='one'
transitions=[
	['12', 'one', 'two'],
	['23', 'two', 'three'],
	['31', 'three', 'one']
	]

#(name, source, dest, conditions=None, unless=None, before=None, after=None, prepare=None)
	
class Test(StateMachine):
	def __init__(self):
		StateMachine.__init__(self, states, initial, transitions, prepare_event='prepare')
		
	def prepare(self, event): pass
		
test=Test()
test.onEvent(object)
test.onEvent(object)
test.onEvent(object)