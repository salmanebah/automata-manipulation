# Automata manipulation
A library for automata manipulation. Requires dotty for the display of the automata. 
## Features
- Check whether an automaton is complete or not
- Check whether an automaton is deterministic or not
- Complete an automaton
- Compute the mirror of an automaton
- Suppress epsilon transitions of an automaton
- Determinize an automaton
- Compute the complement of an automaton
- Compute the union of two automata
- Compute the intersection of two automata
- Minimize an automaton by either using the Moore or the Brzozowski algorithm
- Convert a regular expression to an equivalent automaton by using the Thompson algorithm

## Example
Completing and minimizing an automaton
```python
from automaton_manipulation import *
a = automaton(alphabet=['a', 'b', 'c'],
              initials=[0],
              finals=[2],
			  transitions=[(0, 'a', 1), (0, 'b', 0), (1, 'c', 0), (2, 'b', 0)])
a.display()
b = completer(a)
b.display(wait=True)
c = minimiser(b)
c.display(wait=True)
```
see the file `automaton_manipulation_test` for further examples.
