# CSPy
General-purpose Python solver for constraint satisfaction problems.
Useful for anything that can be formulated as a CSP, such as scheduling or Sudoku.

### Installation
```
git clone https://github.com/ohjay/cspy.git
cd cspy
python setup.py develop
```

### Usage
In general, CSPs are defined by their variables, domains, and constraints. In `CSPy`, each variable
is represented as a `Variable` object which also encodes the associated domain as a set of values.
Upon construction, a `Variable` takes a name (to be used as an identifier) and an initial set of possible values:

```python
from cspy import Variable
var_ts0 = Variable('teaching_slot_8am', {'Robin', 'Evan', 'Chris'})
```

Meanwhile, each constraint is represented as a tuple of N variable names
(note: the string names, not the actual variables!) and a _function_ which takes in those N variables
and returns either True or False, depending on whether or not the constraint is satisfied.

```python
from cspy import Constraint
constraint0 = Constraint(('teaching_slot_8am',), lambda var_ts0: var_ts0 != 'Evan')
```

Constructors for common constraints, such as uniqueness (where no two variables can have the same value)
have been predefined in `common_constraints`. Each constraint constructor takes in a list of variable names
(and sometimes additional constraint-specific keyword args). Accordingly, once imported
(via `from cspy.common_constraints import <NAME>`), one of these constructors can be used to create a constraint
by then calling `<NAME>(var_names, **kwargs)`. At the time of writing,
supported constraint constructors (+ signatures) include

- `uniqueness(var_names)`

In the `CSPy` interface, all constructs are tied together through the `CSP` class.
A `CSP` object represents a constraint satisfaction problem in full, and contains methods
for adding both variables and constraints to the represented problem.

```python
from cspy import CSP
csp = CSP()
csp.add_variable(var_ts0)
csp.add_constraint(constraint0)
```

Once the problem has been defined, solutions can be obtained via `csp.get_solution()` or `csp.get_all_solutions()`.

```python
soln = csp.get_solution(algorithm='backtracking')  # which here would return either 'Robin' or 'Chris'
```

### Examples
#### N-queens
```python
from cspy import *
# TODO
```

#### Sudoku
As a toy example, we will solve [this game](examples/sudoku.png).
```python
from cspy import *
# TODO
```
