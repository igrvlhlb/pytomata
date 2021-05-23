# Non-deterministic Pushdown Automaton

To have access to the `NPDA` class, you should
```python
from pytomaton.npda import NPDA
```
For creating an instance of a `NDFA` you have to provide it:
- the input alphabet
- the states
- the initial state
- final states
- the transitions (a `dict`)
- the acceptance criterion or criteria, where:
    - 'both' means 

`NPDA`s are somewhat similar to `NDFA`s, but there is a key difference: it works with the aid of a stack.<br>
For this automaton we will keep using the concept of a clock -- where each tick represents one input symbol consumed.<br>
`NPDA`s also have epsilon-transitions, but now the transition function have more elements:
- for the input, we have to consider an input symbol to read and a symbol to pop from the top of the stack
- for the output, we have the set of next states with which symbol or word to push onto the top of the stack

the stack elements of the transition function can also be '&' -- as an argument it means "do not check
the top of the stack" and as result it means "do not push anything onto the stack".

Let's see an example: the `NPDA` that accepts the language `0^(2k)1^k`, for `k >= 0`

<!-- ![NDFA Graph](dot/ndfa.svg) -->

and its corresponding code

```python
from pytomaton.ndfa import NDFA


npda = NPDA(
    alphabet={'0','1'},
    stack_alphabet={'0','1'},
    states={'q1', 'q2', 'q3'},
    initial_state='q1',
    final_states={'q2'},
    transitions={
        'q1': {
            # does not read the input
            '&': {
                # neither pop nor push anything and goes to the state 'q2'
                '&': {('q2', '&')},
            },
            # reads 0 from the input
            '0': {
                # doesnt check the stack and pushes 0, then goes to 'q1'
                '&': {('q1', '0')},
            }
        },
        'q2': {
            # if there is a 1 in the input
            '1': {
                # pop 0 from the stack and doesnt push anything and goes to 'q3'
                '0': {('q3', '&')}
            },
        },
        'q3': {
            # doesnt read the input
            '&': {
                # pops 0 from the stack, doesnt push anything and goes to 'q2'
                '0': {('q2', '&')}
            }
        }
    },
    acceptance_mode='both'
)

```

For checking if the authomaton accepts certain word, call `npda.accepts(<word>)`, that returns a boolean.

```python
```

If you wish to see the execution step by step, call `ndfa.read(<word>, show_steps=True)`. If you are only
interested in the final states and the input symbols not read, call it without the `show_steps` argument.<br>
When reading the steps, you may face more than one current state. That is because of the non-determinism
of the `NDFA`. In this simulator, we use the concept of a clock so that we can easily know in which step
we are in the moment. Each tick of the clock corresponds to one input symbol consumed. In the case of
non-deterministic automata, we make all the possible epsilon-transitions before the clock ticks.
Here is an example of that:

```python
>>> ndfa.read('001', show_steps=True)
Clock: 0, Current States: ['q1', 'q5', 'q2', 'q3'], Remaining Input: '001'
Clock: 1, Current States: ['q4', 'q3'], Remaining Input: '01'
Clock: 2, Current States: ['q4', 'q3'], Remaining Input: '1'
Clock: 2, Current States: ['q4', 'q3'], Remaining Input: '1'
('1', ['q4', 'q3'])
```
notice that the last line is the return value from the call to `ndfa.read(<word>)`
```python
>>> dfa.read('001')
('1', ['q4', 'q3'])
```

For a word to be accepted by a `NDFA` it suffices to have **at least** one final state among the states
returned by `ndfa.read(<word>)` (the reachable states for the ginven input word)