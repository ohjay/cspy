#!/usr/bin/env python

"""
__init__.py

Represents the constraint satisfaction problem (CSP) interface.
Full import: `from cspy import Variable, Constraint, CSP`
"""

import pprint
from cspy.solver import Solver


class Variable(object):
    """A variable.
    If involved in a CSP, the goal will be to assign this variable a value that satisfies the constraints
    and possibly works together with other variables to maximize or minimize an objective value.
    """
    def __init__(self, name, domain=(), value=None):
        self.name = name
        self.domain = domain
        self.value = value  # in theory, only the solver should assign this attribute

    @staticmethod
    def parse_value(var):
        return var.value if isinstance(var, Variable) else var

    def __repr__(self):
        return 'cspy.Variable(%r)' % self.__dict__

    def __str__(self):
        return 'a CSPy Variable with attributes %r' % self.__dict__

    def __lt__(self, other):
        return self.value < Variable.parse_value(other)

    def __le__(self, other):
        return self.value <= Variable.parse_value(other)

    def __eq__(self, other):
        return self.value == Variable.parse_value(other)

    def __ne__(self, other):
        return self.value != Variable.parse_value(other)

    def __gt__(self, other):
        return self.value > Variable.parse_value(other)

    def __ge__(self, other):
        return self.value >= Variable.parse_value(other)

    def __contains__(self, value):
        return value in self.domain

    def __len__(self):
        return len(self.domain)

    def __abs__(self):
        return abs(self.value)

    def __add__(self, other):
        return self.value + Variable.parse_value(other)

    def __and__(self, other):
        return self.value and Variable.parse_value(other)

    def __bool__(self):
        return bool(self.value)

    def __int__(self):
        return int(self.value)

    def __mod__(self, other):
        return self.value % Variable.parse_value(other)

    def __mul__(self, other):
        return self.value * Variable.parse_value(other)

    def __neg__(self):
        return -self.value

    def __nonzero__(self):
        return bool(self.value)

    def __or__(self, other):
        return self.value or Variable.parse_value(other)

    def __sub__(self, other):
        return self.value - Variable.parse_value(other)

    def __truediv__(self, other):
        return self.value / Variable.parse_value(other)


class Constraint(object):
    """A constraint.
    A constraint specifies allowable combinations of values for a subset of variables;
    in `CSPy`, every constraint is represented by (a) an ordered tuple of variable names
    and (b) a function which takes in the variables associated with those names
    and returns True or False depending on whether or not the constraint has been met.
    """
    def __init__(self, var_names, satisfied):
        try:
            self.var_names = tuple(var_names)  # names of variables involved in the constraint
        except TypeError:
            self.var_names = (var_names,)
            print('WARNING: `var_names` is not a collection; casting it to one automatically')
        self.satisfied = satisfied  # fn: (vars, in order specified by `var_names`) -> True/False

    def __contains__(self, value):
        """Check whether or not a variable (identified by its name) is involved in the constraint."""
        return value in self.var_names


class CSP(object):
    """A constraint satisfaction problem (CSP).
    A CSP is defined over a set of variables and constraints, and involves assigning a value to each variable
    s.t. all of the constraints are satisfied and an objective function, if one exists, is maximized.
    """
    def __init__(self, variables=(), constraints=(), objective_fn=None):
        self.var_list = list(variables)
        self.var_dict = {var.name: var for var in variables}
        self.constraints = list(constraints)
        self.objective_fn = objective_fn

    def add_variable(self, var):
        """Adds a variable to the registry of the CSP."""
        self.var_list.append(var)
        self.var_dict[var.name] = var

    def add_constraint(self, constraint):
        """Adds a constraint to the registry of the CSP."""
        self.constraints.append(constraint)

    def set_objective_fn(self, objective_fn):
        """Assigns an objective function to the CSP.
        An objective function should take in all variables
        and return a scalar representing the quantity to be maximized."""
        self.objective_fn = objective_fn

    def get_solution(self, algorithm='backtracking'):
        """Returns the optimal solution as defined by the constraints and the objective function.
        If no objective function exists, returns an arbitrary valid solution.
        If no solution exists (i.e. the feasible set is empty), returns None.
        """
        return Solver(self).solve(algorithm=algorithm, take_first=True)

    def get_all_solutions(self, algorithm='backtracking'):
        """Returns all solutions to the CSP.
        If an objective function exists, this will return all optimal solutions.
        If no objective function exists, this will return all valid solutions.
        """
        return Solver(self).solve(algorithm=algorithm, take_first=False)

    def all_variables_assigned(self):
        return all(var.value is not None for var in self.var_list)

    def print_current_assignment(self):
        pprint.pprint({var.name: var.value for var in self.var_list if var.value is not None})
