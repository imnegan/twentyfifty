# coding=utf-8
'''
state_machine
by Paul Egan imnegan@gmail.com
'''

from random import random


class State(object):
    """ A state initialised by a string"""

    def __init__(self, name):
        self.name = name
        self.transitions = set()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name + ':' + str(self.transitions)


class Transition:
    """
    The pathway from a source state to destination state.
    If the condition is met the action is executed.
    """

    def __init__(self, state_machine, name, source, dest, condition=None, action=None):
		#TODO: add before and after actions
        self.state_machine = state_machine
        self.name = name
        self.source = source
        self.dest = dest
        self.condition = condition
        self.action = action

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class StateMachine:
    """
    Main class, contains states, transitions, condition methods and action methods
    """

    def __init__(self, name='state machine', states=None, transitions=None, initial=None):
        self.name = name
        self.states = dict()
        for _s in states:
            self.states[_s] = State(_s)
        if initial is not None:
            self.states[initial] = State(initial)
            self.state = self.states[initial]
        else:
            self.state = self.states[states[0]]
        for _t in transitions:
            self.add_transition(_t)

    def true_condition(self):
        """default condition that is automatically assigned to transitions"""
        return True

    def pass_action(self):
        """
        default action that is automatically assigned to transitions.
        does nothing.
        """
        pass

    def add_transition(self, transition):
        """creates a Transition object from a list"""
        if transition[1] == '*':
            pass  # TODO
        else:
            name = transition[0]
            from_state = self.states[transition[1]]
            to_state = self.states[transition[2]]

            # condition TODO: listify then run multiple conditions
            if len(transition) > 3:
                condition = getattr(self, transition[3])
            else:
                condition = self.true_condition

            # action
            if len(transition) > 4:
                action = getattr(self, transition[4])
            else:
                action = self.pass_action

            _t = Transition(self, name, from_state,
                            to_state, condition, action)
            from_state.transitions.add(_t)

    def run(self):
        """
        1. evaluates condition for each transition. if true:
        2. executes action
        3. changes state
        """

        print('Start state:', self.state)
        for transition in self.state.transitions:
            print('Testing transition:', transition)
            if transition.condition() is True:
                transition.action()
                self.state = transition.dest
                break
