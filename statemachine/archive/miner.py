from state_machine import StateMachine

class Miner(StateMachine):
    """example state machine that mines stuff and brings stuff back, repeat"""

    stateList = ['fossicking', 'going', 'mining', 'returning', 'unloading']
    transitionList = [
        ['found_target', 'fossicking', 'going', 'random_condition'],
        ['arrived', 'going', 'mining', 'random_condition'],
        ['not_finished_mining', 'mining', 'mining',
         'not_finished_mining_condition', 'mine'],
        ['finished_mining', 'mining', 'returning', 'finished_mining_condition'],
        ['arrived', 'returning', 'unloading', 'random_condition'],
        ['holdEmpty', 'unloading', 'fossicking', 'random_condition']
    ]
    initial = 'fossicking'

    def __init__(self, name='miner'):
        StateMachine.__init__(self, name, Miner.stateList,
                              Miner.transitionList, Miner.initial)
        self.qty = 0
        self.capacity = 10

    # conditions
    def finished_mining_condition(self):
        """true if miner is at capacity"""
        print('qty:', self.qty)
        return self.qty == self.capacity

    def not_finished_mining_condition(self):
        """true if there is still space"""
        print('qty:', self.qty)
        return self.qty < self.capacity

    def random_condition(self):
        """true if random number is > 0.5"""
        _r = random()
        return _r > 0.5

    # actions
    def mine(self):
        """collect some stuff"""
        print('Action: mine 1')
        self.qty += 1


miner = Miner()

print('fin')
