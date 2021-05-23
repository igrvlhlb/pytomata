# Non-deterministic Finite Automaton

To have access to the `NDFA` class, you should
```python
from pytomaton.ndfa import NDFA
```
For creating an instance of a `NDFA` you have to provide it:
- the input alphabet
- the states
- the initial state
- final states
- the transitions (a `dict`)

`NDFA`s don't have the same restrictions as `DFA`s have. e.g. you do not have to write one transition
for each possible input symbol for every state. Also, you can have more than one transition for the
same state and input symbol. In other words, given a state `q` and an input symbol `i`, you can have
0 or more transitions from `q` consuming `i` from the input word.<br>
Another characteristic of `NDFA`s is that you can have epsilon-transitions -- transitions that do not
read any input symbols. Epsilon is denoted by the character '&'.

Let's take as an example this automaton that accepts the language `0* U 1`

![NDFA Graph](dot/ndfa.svg)

and its corresponding code
```python
from pytomaton.ndfa import NDFA

alphabet = ['0', '1']
states = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
initial = 'q1'
finals = {'q2', 'q4', 'q6'}
transitions = {
    'q1': {
        '&': {'q2', 'q5'} # two possible epsilon-transitions from the state 'q1'
    },
    'q2': {
        '&': {'q3'}
    },
    'q3': {
        '0': {'q4'}
    },
    'q4': {
        '&': {'q3'}
    },
    'q5': {
        '1': {'q6'}
    }
}

ndfa = NDFA(alphabet, states, initial, finals, transitions)
```

For checking if the authomaton accepts certain word, call `ndfa.accepts(<word>)`, that returns a boolean.

```python
>>> dfa.accepts('')
True
>>> ndfa.accepts('1')
True
>>> ndfa.accepts('00')
True
>>> ndfa.accepts('000000000')
True
>>> ndfa.accepts('001')
False
>>> ndfa.accepts('10')
False
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