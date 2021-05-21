import ndfa

class DFA(ndfa.NDFA):
    def is_valid(self):
        if super().is_valid() is False:
            return False
        visited_states = self.states.copy()
        for state, transition in self.transitions.items():
            visited_states.remove(state)
            visited_symbols = self.alphabet.copy()
            for symbol, states in transition.items():
                visited_symbols.remove(symbol)
                if len(states) != 1 or symbol == '&':
                    return False
            if len(visited_symbols) != 0:
                return False
        if len(visited_states) != 0:
            return False
        return True