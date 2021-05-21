from automaton import InvalidStateError, InvalidSymbolError, InvalidTransitionError
from ndfa import NDFA

class DFA(NDFA):
    def is_valid(self):
        remaining_states = self.states.copy()
        for state, transition in self.transitions.items():
            remaining_states.remove(state)
            remaining_symbols = self.alphabet.copy()
            for symbol, states in transition.items():
                remaining_symbols.remove(symbol)
                if len(states) != 1:
                    raise InvalidTransitionError(states,
                    "DFAs should have only one transition per symbol,\
                    but these {} possibilities were found")
                if symbol == '&':
                    raise InvalidSymbolError(symbol, "{} is meant to represent epsilon and\
                        should not be used otherwise")
            if len(remaining_symbols) != 0:
                raise InvalidTransitionError(remaining_symbols,
                "DFAs should have excactly one transition per symbol,\
                    but these were missing: {}")
        if len(remaining_states) != 0:
            raise InvalidTransitionError(remaining_states,
                "DFAs should have transitions for all states, but these don't have: {}")