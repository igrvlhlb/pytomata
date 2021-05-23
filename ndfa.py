from .automaton import Automaton,\
    InvalidStateError, InvalidSymbolError, InvalidTransitionError

class NDFA(Automaton):

    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        super().__init__(alphabet,states,initial_state,final_states,transitions)
        self._validate()

    def transition(self, state, symbol):
        if self.transitions.get(state) is not None:
            if self.transitions[state].get(symbol) is not None:
                return self.transitions[state][symbol]
        return None

    def read(self, input, show_steps=False):

        current_states = [self.initial_state]
        syms = [sym for sym in input]  # separate the input symbols
        clock = 0

        while len(syms) != 0:
            next_states = []
            for state in current_states:
                # make all the epsilon-transitions
                epsT = self.transition(state, '&')
                if epsT is not None:
                    for s in epsT:
                        if s not in current_states:
                            current_states.append(s)
            if show_steps is True:
                self._show_config(clock, current_states,''.join(syms))
            sym = syms.pop(0)
            found_transition = False
            for state in current_states:
                # consume one input symbol
                symT = self.transition(state, sym)
                if symT is not None:
                    found_transition = True
                    for s in symT:
                        if s not in next_states:
                            next_states.append(s)
            if found_transition == False:
                syms.insert(0, sym)
            if next_states == []:
                break
            current_states = next_states
            clock += 1
        # we need to make the epsilon-transitions after
        # there is no more input symbols to consume
        for state in current_states:
                # make all the epsilon-transitions
                epsT = self.transition(state, '&')
                if epsT is not None:
                    for s in epsT:
                        if s not in current_states:
                            current_states.append(s)
        if show_steps is True:
            self._show_config(clock, current_states,''.join(syms))
        return (''.join(syms), current_states)

    def accepts(self, input):
        remaining_input, states = self.read(input)
        reached_finals = self.final_states.intersection(set(states))
        if len(remaining_input) == 0 and len(reached_finals) != 0:
            return True
        else:
            return False

    def _show_config(self, clock, states, input):
        print('Clock: {}, Current States: {}, Remaining Input: \'{}\''.format(clock, states, input))

    def _validate(self):
        for state, transition in self.transitions.items():
            if state not in self.states:
                raise InvalidStateError(state, "{} is not in the state set")
            for symbol, states in transition.items():
                if symbol not in self.alphabet and symbol != '&':
                    raise InvalidSymbolError(symbol, "{} is not on the input alphabet")
                if not states.issubset(self.states):
                    raise InvalidStateError(states, "{} is not a subset of the states set")