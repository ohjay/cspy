#!/usr/bin/env python

"""
common_constraints.py

Common constraints, predefined for convenience.

A constraint specifies allowable combinations of values for a subset of variables;
in `CSPy`, every constraint takes in a dictionary containing all of the variables
and returns True or False depending on whether or not the constraint has been met.
"""

from cspy import Constraint


def uniqueness(var_names):
    """Creates a Constraint on the given variable names which specifies
    that all of the associated variables must be assigned different values.
    """
    def _satisfied(*var_list):
        values = [var.value for var in var_list if var.name in var_names]
        if None in values:
            return True  # not qualified to make a decision yet
        return len(values) == len(set(values))
    return Constraint(var_names, _satisfied)
