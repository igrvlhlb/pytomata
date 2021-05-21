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