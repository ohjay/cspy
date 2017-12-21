#!/usr/bin/env python

"""
solver.py

Constraint satisfaction problem (CSP) solver.
Options for solver algorithms:
- backtracking
"""

import copy
import itertools


class Solver(object):
    """A solver.
    A solver should be able to determine the solution set for a CSP.
    """
    def __init__(self, csp):
        self.csp = csp
        self.ALGORITHMS = {
            'backtracking': self.backtracking,
            'min_conflicts': self.min_conflicts,
        }

    def solve(self, algorithm='backtracking', take_first=True):
        """Finds solutions to the solver's assigned CSP.
        If TAKE_FIRST is True, returns the first observed solution that is both optimal and valid.
        Otherwise, returns the set of all solutions.
        """
        try:
            self.ALGORITHMS[algorithm](take_first)
        except KeyError:
            raise NotImplementedError('algorithm %r not supported!' % algorithm)

    ###################################
    # BACKTRACKING SEARCH + UTILITIES #
    ###################################

    def backtracking(self, take_first=True):
        """Backtracking search with forward checking.
        Returns the solution (or, if TAKE_FIRST is False, the set of all solutions) to the CSP given by `self.csp`.
        If no solutions exist, returns False.
        """
        _csp = copy.deepcopy(self.csp)
        assignments = []

        # Order domains (we only want to do this once)
        _domains = {}
        for var in _csp.var_list:
            _domains[var] = self.order_domain(var, _csp)

        # TODO
        assignment = []
        while len(assignment) < len(_csp.var_list):
            next_var = self.select_unassigned_var(_csp.var_list)
            # make sure this doesn't keep choosing the same variable

    @staticmethod
    def select_unassigned_var(var_list):
        """Choose the variable from VAR_LIST with the fewest values remaining in its domain."""
        return min(var_list, key=lambda x: len(x.domain))

    def order_domain(self, var, csp):
        """Orders VAR's domain by a least constraining metric
        (non-destructive; the ordered domain will be returned).
        """
        other_vars = [_v for _v in csp.var_list if _v.name != var.name]

        def _num_pruned(value):
            """If the value VALUE is chosen for VAR, see/return how many values in total are pruned
            from the domains of other variables.
            """
            init_total = sum([len(_v.domain) for _v in other_vars])
            _other_vars = copy.deepcopy(other_vars)
            for constraint in csp.constraints:
                if var.name not in constraint.var_names:
                    continue
                __other_vars = [_v for _v in _other_vars if _v.name in constraint.var_names]
                for other_var in __other_vars:
                    invalid_values = []
                    for other_value in other_var.domain:
                        other_var.value = other_value
                        partial_modified = self._make_assignment([var, other_var], [value, other_value])
                        partial_assignment = {var.name: var, other_var.name: other_var}

                        # Is (var = VALUE, other_var = OTHER_VALUE) a valid assignment?
                        # If not, prune OTHER_VALUE from the domain of `other_var`
                        valid = False
                        remaining_vars = [_v for _v in __other_vars if _v is not other_var]
                        if remaining_vars:
                            for remaining_values in itertools.product([list(_v.domain) for _v in remaining_vars]):
                                remaining_modified = self._make_assignment(remaining_vars, remaining_values)
                                assignment = self.merge_dicts(
                                    partial_assignment, dict([(_v.name, _v) for _v in remaining_vars]))
                                arg_list = [assignment[name] for name in constraint.var_names]
                                if constraint.satisfied(*arg_list):
                                    valid = True
                                self._make_assignment(*remaining_modified)  # undo "remaining" assignment
                                if valid:
                                    break
                        elif constraint.satisfied(*[partial_assignment[name] for name in constraint.var_names]):
                            valid = True
                        if not valid:
                            invalid_values.append(other_value)
                        self._make_assignment(*partial_modified)  # undo "partial" assignment
                    other_var.domain = [_value for _value in other_var.domain if _value not in invalid_values]
            return init_total - sum([len(_v.domain) for _v in _other_vars])

        return sorted(list(var.domain), key=lambda x: _num_pruned(x))

    @staticmethod
    def _make_assignment(var_list, values):
        """Makes the assignment.
        Returns a list of modified variables and their previous values.
        """
        modified_vars, previous_values = [], []
        for var, value in zip(var_list, values):
            if var.value != value:
                modified_vars.append(var)
                previous_values.append(var.value)
                var.value = value
        return modified_vars, previous_values

    @staticmethod
    def merge_dicts(*args):
        z = args[0].copy()  # start with the first dictionary's keys and values
        for y in args[1:]:
            z.update(y)  # modifies z with y's keys and values & returns None
        return z


    #################
    # MIN CONFLICTS #
    #################

    def min_conflicts(self, take_first=True):
        """Local search / iterative improvement.
        Solves the CSP given by `self.csp`.
        """
        _csp = copy.deepcopy(self.csp)
        # TODO
