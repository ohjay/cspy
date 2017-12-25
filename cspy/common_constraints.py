#!/usr/bin/env python

"""
common_constraints.py

Common constraints, predefined for convenience.

A constraint specifies allowable combinations of values for a subset of variables;
in `CSPy`, every constraint takes in a dictionary containing all of the variables
and returns True or False depending on whether or not the constraint has been met.
"""

import itertools
from cspy import Constraint


def uniqueness(var_names, pairwise=False):
    """Creates a Constraint on the given variable names which specifies
    that all of the associated variables must be assigned different values.

    If PAIRWISE is True, this will return a list of pairwise inequality Constraints.
    Otherwise returns a single uniqueness Constraint.
    """
    if pairwise:
        return [inequality(name0, name1) for name0, name1 in itertools.combinations(var_names, 2)]
    def _satisfied(*var_list):
        values = [var.value for var in var_list if var.name in var_names]
        if None in values:
            return True  # not qualified to make a decision yet
        return len(values) == len(set(values))
    return Constraint(var_names, _satisfied, name='uniqueness')


def inequality(name0, name1):
    """Creates a Constraint on the two variables which specifies that their values must be different."""
    return Constraint((name0, name1), lambda v0, v1: v0.value != v1.value)
