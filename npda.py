from automaton import Automaton

class NPDA(Automaton):
    
    def __init__(self, alphabet, stack_alphabet, states, initial_state, final_states, transitions, acceptance_mode):
        super().__init__(alphabet, states, initial_state, final_states, transitions)
        self.acceptance_mode = acceptance_mode

    def transition(self, state, symbol, stack_top):
        transition_set = set()
        tState = self.transitions.get(state)
        if tState is not None:
            tSymbol = tState.get(symbol)
            if tSymbol is not None:
                tST = tSymbol.get(stack_top)
                if tST is not None:
                    for to, push in tST:
                        if push == '&':
                            push_symbol = ''
                        else:
                            push_symbol = push
                        tup = (to, Stack(push_symbol))
                        transition_set.add(tup)
                    return transition_set
                    
        return None

    def read(self, input, show_steps=False):

        # now the states are state-stack tuples
        current_states = [(self.initial_state, Stack())]
        syms = [sym for sym in input]  # separate the input symbols
        clock = 0

        while len(syms) != 0:
            next_states = []
            if show_steps is True:
                self._show_config(clock, current_states,''.join(syms))
            for state, stack in current_states:
                # make all the epsilon-epsilon transitions
                eps2T = self.transition(state, '&', '&')
                if eps2T is not None:
                    for s, st in eps2T:
                        next_stack = stack.chain(st)
                        if (s, next_stack) not in current_states:
                            current_states.append((s, next_stack))
                # make all the epsilon-stack_top transitions
                epsT = self.transition(state, '&', stack.peek())
                if epsT is not None:
                    stack_copy = Stack(stack)
                    stack_copy.pop()
                    for s, st in epsT:
                        next_stack = stack_copy.chain(st)
                        if (s, next_stack) not in current_states:
                            current_states.append((s, next_stack))

            sym = syms.pop(0)
            found_transition = False
            # transitions that consume input symbols
            for state, stack in current_states:
                # consume one input symbol
                symT = self.transition(state, sym, stack.peek())
                if symT is not None:
                    found_transition = True
                    stack_copy = Stack(stack)
                    stack_copy.pop()
                    for s, st in symT:
                        next_stack = stack_copy.chain(st)
                        if (s, next_stack) not in next_states:
                            next_states.append((s, next_stack))
                symE = self.transition(state, sym, '&')
                if symE is not None:
                    found_transition = True
                    for s, st in symE:
                        next_stack = stack.chain(st)
                        if (s, next_stack) not in next_states:
                            next_states.append((s, next_stack))

            if found_transition == False:
                syms.insert(0, sym)
            if next_states == []:
                break
            current_states = next_states
            clock += 1
        # we need to make the epsilon-transitions after
        # there is no more input symbols to consume
        for state, stack in current_states:
            # make all the epsilon-epsilon transitions
            eps2T = self.transition(state, '&', '&')
            if eps2T is not None:
                for s, st in eps2T:
                    next_stack = stack.chain(st)
                    if (s, next_stack) not in current_states:
                        current_states.append((s, next_stack))
            # make all the epsilon-stack_top transitions
            epsT = self.transition(state, '&', stack.peek())
            if epsT is not None:
                stack_copy = Stack(stack)
                stack_copy.pop()
                for s, st in epsT:
                    next_stack = stack_copy.chain(st)
                    if (s, next_stack) not in current_states:
                        current_states.append((s, next_stack))
        if show_steps is True:
            self._show_config(clock, current_states,''.join(syms))
        return (''.join(syms), current_states)
    
    def accepts(self, input):
        remaining_input, states = self.read(input)
        if len(remaining_input) != 0:
            return False
        for state, stack in states:
            if self.acceptance_mode in ('final_state', 'either'):
                if state in self.final_states:
                    return True
            elif self.acceptance_mode in ('empty_stack', 'either'):
                if len(stack) == 0:
                    return True
            else:
                if state in self.final_states and len(stack) == 0:
                    return True
        return False

    def _show_config(self, clock, states, input):
        print('Clock: {}, Current (States, Stacks): {}, Remaining Input: \'{}\''\
            .format(clock, states, input))
    
class Stack:
    
    def __init__(self, lst=[]):
        if isinstance(lst, str):
            self.stack = [c for c in reversed([cc for cc in lst])]
        elif isinstance(lst, Stack):
            self.stack = lst.stack.copy()
        else:
            self.stack = [e for e in reversed(lst)]

    def push(self, lst):
        if isinstance(lst, str):
            if lst == '&':
                return
            for c in reversed([cc for cc in lst]):
                self.stack.append(c)
        else:
            for e in reversed(lst):
                self.stack.append(e)

    def pop(self):
        if len(self.stack) != 0:
            return self.stack.pop()
        else:
            return '&'

    def peek(self):
        if len(self.stack) != 0:
            return self.stack[-1]
        else:
            return '&'

    # non-destructive chaining
    def chain(self, other):
        if isinstance(other, Stack):
            return Stack(list(reversed(self.stack + other.stack)))
        else:
            new_stack = Stack(self)
            if other != '&':
                new_stack.push(other)
            return new_stack # only a copy of self
    
    def _joined(self):
        return ''.join(reversed(self.stack))

    def __len__(self):
        return len(self.stack)
    
    def __str__(self):
        #return "NPDAStack({})".format(list(reversed(self.stack)))
        return "NPDAStack({})".format(self._joined())
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Stack):
            if self.stack == o.stack:
                return True
        return False
    
    def __hash__(self) -> int:
        # as a list is not hashable, we return
        # the hash of the tuple built from that list
        return hash(tuple(self.stack))