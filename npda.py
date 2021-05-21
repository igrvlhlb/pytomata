from automaton import Automaton

class NPDA(Automaton):
    
    def __init__(self, alphabet, stack_alphabet, states, initial_state, final_states, transitions):
        super.__init__(alphabet, states, initial_state, final_states, transitions)
        self.stack = []
        self.stack_alphabet = set(stack_alphabet)

    def transition(self, state, symbol, stack_top):
        transition_set = set()
        tState = self.transitions.get(state)
        if tState is not None:
            tSymbol = tState.get(symbol)
            if tSymbol is not None:
                tST = tSymbol.get(stack_top)
                if tST is not None:
                    for to, push in tST:
                        tup = (to, Stack(push))
                        transition_set.add(tup)
                    return transition_set
                    
        return None
    
class Stack:
    
    def __init__(self, lst=[]):
        if isinstance(lst, str):
            self.stack = [c for c in reversed([cc for cc in lst])]
        else:
            self.stack = [e for e in reversed(lst)]

    def push(self, lst):
        if isinstance(lst, str):
            for c in reversed([cc for cc in lst]):
                self.stack.append(c)
        else:
            for e in reversed(lst):
                self.stack.append(e)

    def pop(self):
        return self.stack.pop()

    # non-destructive chaining
    def chain(self, other):
        return self.stack + other.stack

    def __len__(self):
        return len(self.stack)
    
    def __str__(self):
        return "NPDAStack({})".format(list(reversed(self.stack)))
    
    def __repr__(self):
        return self.__str__()