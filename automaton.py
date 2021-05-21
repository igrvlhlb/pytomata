class Automaton:
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        self.alphabet = set(alphabet)
        self.states = set(states)
        self.initial_state = initial_state
        self.final_states = set(final_states)
        self.transitions = transitions

    def __str__(self):
        return '(Alphabet: {}, States: {}, Initial State: {}, Final States: {}, Transitions: {})'\
        .format(self.alphabet, self.states, self.initial_state, self.final_states, self.transitions)
    
    def __repr__(self):
        return self.__str__()
    
class InvalidStateError(Exception):
    def __init__(self, state):
        self.__state = state
    def __str__(self):
        return '{} is not a valid state name'.format(self.__state)

class InvalidSymbolError(Exception):
    def __init__(self, symbol):
        self.__symbol = symbol
    def __str__(self):
        return '{} does not belong to the input alphabet'.format(self.__symbol)

class InvalidStackSymbolError(InvalidSymbolError):
    def __str__(self):
        return super.__str__().replace('input', 'stack')