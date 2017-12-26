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
**Note:** constraint formulation makes a huge difference. Try to minimize the number of variables
involved in each constraint.

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
- `inequality(name0, name1)`
- `inequality_unary(name, constant)`

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
import itertools
from cspy import Variable, Constraint, CSP
N = 8
csp = CSP()
var_names = []
for i in range(N):
    var_names.append(str(i))
    csp.add_variable(Variable(str(i), [(r, c) for r in range(N) for c in range(N)]))
for names in itertools.combinations(var_names, 2):
    csp.add_constraint(Constraint(names, lambda v0, v1: v0.value[0] != v1.value[0]))
    csp.add_constraint(Constraint(names, lambda v0, v1: v0.value[1] != v1.value[1]))
    csp.add_constraint(Constraint(names, lambda v0, v1: abs(v0.value[0] - v1.value[0]) != abs(v0.value[1] - v1.value[1])))
soln = csp.get_solution(algorithm='min_conflicts')
```

#### Sudoku
The code given [here](https://github.com/ohjay/cspy/blob/master/examples/sudoku.py) will solve [this game](examples/sudoku.png).
