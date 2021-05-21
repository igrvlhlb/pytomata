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

    def _validate(self):
        # '&' is a special symbol that denotes epsilon
        # and should only be used in transitions
        for token in self.alphabet\
            .union(self.states)\
            .union({self.initial_state})\
            .union(self.final_states):
            if len(token) == 0 or token.isspace() or token == '&':
                if token in self.__alphabet:
                    raise InvalidSymbolError(token, "{} is not a valid symbol")
                else:
                    raise InvalidStateError(token, "{} is not a valid state name")
            

class BaseAutomatonError(Exception):
    def __init__(self, var, msg):
        self.__var = var
        self.__msg = msg
    def __str__(self):
        return self.__msg.format(repr(self.__var))

class InvalidStateError(BaseAutomatonError):
    pass
class InvalidSymbolError(BaseAutomatonError):
    pass