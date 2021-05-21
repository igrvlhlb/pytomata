from automaton import Automaton

class NDFA(Automaton):

    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        super.__init__(alphabet,states,initial_state,final_states,transitions)

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
            if show_steps is True:
                self._show_config(clock, current_states,''.join(syms))
            for state in current_states:
                # make all the epsilon-transitions
                epsT = self.transition(state, '&')
                if epsT is not None:
                    for s in epsT:
                        if s not in current_states:
                            current_states.append(s)
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

    # return True if the automaton
    # is valid or False otherwise
    def is_valid(self):
        # '&' is a special symbol
        # that denotes epsilon
        for token in self.alphabet\
            .union(self.states)\
            .union({self.initial_state})\
            .union(self.final_states):
            if len(token) == 0 or token.isspace() or token == '&':
                print("Falhou primeiro for")
                return False
        for state, transition in self.transitions.items():
            if state not in self.states:
                return False
            for symbol, states in transition.items():
                if symbol not in self.alphabet and symbol != '&'\
                    or len(set(states).difference(self.states)) != 0:
                    print(self.alphabet, symbol, set(states).difference(self.states))
                    print("Falhou Segundo For")
                    return False
        return True