#!/usr/bin/env python

"""
solver.py

Constraint satisfaction problem (CSP) solver.
Options for solver algorithms:
- backtracking
"""

import copy
import itertools
from cspy.utils import timed, merge_dicts


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

    @timed('The search')
    def solve(self, algorithm='backtracking', take_first=True):
        """Finds solutions to the solver's assigned CSP.
        If TAKE_FIRST is True, returns the first observed solution that is both optimal and valid.
        Otherwise, returns the set of all solutions.
        """
        try:
            return self.ALGORITHMS[algorithm](take_first)
        except KeyError:
            raise NotImplementedError('algorithm %r not supported!' % algorithm)

    ###################################
    # BACKTRACKING SEARCH + UTILITIES #
    ###################################

    def backtracking(self, take_first=True, verbose=False):
        """Backtracking search with forward checking.
        Returns the solution (or, if TAKE_FIRST is False, the set of all solutions) to the CSP given by `self.csp`.
        If no solutions exist, returns False.
        """
        _csp = copy.deepcopy(self.csp)
        solutions = []

        # Order domains (we only want to do this once)
        _domains = {}
        for var in _csp.var_list:
            _domains[var.name] = self.order_domain(var, _csp)

        def _recursive_backtracking(_csp):
            if verbose:
                _csp.print_current_assignment()
            if _csp.all_variables_assigned():
                _solution = {var.name: var.value for var in _csp.var_list}
                solutions.append(_solution)
                return _solution
            next_var = self.select_unassigned_var(_csp.var_list)
            for next_value in _domains[next_var.name]:
                if next_value not in next_var.domain:
                    continue
                undo_assign = self.make_assignment([next_var], [next_value])
                if self.consistent(next_var.name, _csp):
                    _solution = _recursive_backtracking(_csp)
                    if _solution is not None and take_first:
                        return _solution
                self.make_assignment(*undo_assign)

        solution = _recursive_backtracking(_csp)
        return solution if take_first else solutions

    @staticmethod
    def select_unassigned_var(var_list):
        """Choose the unassigned variable from VAR_LIST with the fewest values remaining in its domain."""
        return min([var for var in var_list if var.value is None], key=lambda x: len(x.domain))

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
                        undo_partial_assign = self.make_assignment([var, other_var], [value, other_value])
                        partial_assignment = {var.name: var, other_var.name: other_var}

                        # Is (var = VALUE, other_var = OTHER_VALUE) a valid assignment?
                        # If not, prune OTHER_VALUE from the domain of `other_var`
                        valid = False
                        remaining_vars = [_v for _v in __other_vars if _v is not other_var]
                        if remaining_vars:
                            for remaining_values in itertools.product(*[list(_v.domain) for _v in remaining_vars]):
                                undo_remaining_assign = self.make_assignment(remaining_vars, remaining_values)
                                assignment = merge_dicts(
                                    partial_assignment, dict([(_v.name, _v) for _v in remaining_vars]))
                                arg_list = [assignment[name] for name in constraint.var_names]
                                if constraint.satisfied(*arg_list):
                                    valid = True
                                self.make_assignment(*undo_remaining_assign)  # undo "remaining" assignment
                                if valid:
                                    break
                        elif constraint.satisfied(*[partial_assignment[name] for name in constraint.var_names]):
                            valid = True
                        if not valid:
                            invalid_values.append(other_value)
                        self.make_assignment(*undo_partial_assign)  # undo "partial" assignment
                    other_var.domain = [_value for _value in other_var.domain if _value not in invalid_values]
            return init_total - sum([len(_v.domain) for _v in _other_vars])

        return sorted(list(var.domain), key=lambda x: _num_pruned(x))

    @staticmethod
    def make_assignment(var_list, value_list, domain_list=None):
        """Makes the assignment.
        Returns a list of modified variables and their previous values.
        """
        modified_vars, previous_values, previous_domains = [], [], []
        if domain_list is None:
            domain_list = [var.domain for var in var_list]
        for var, value, domain in zip(var_list, value_list, domain_list):
            if var.value != value:
                modified_vars.append(var)
                previous_values.append(var.value)
                previous_domains.append(var.domain)
                var.value = value
                var.domain = {value} if var.value is not None else domain
        return modified_vars, previous_values, previous_domains

    @staticmethod
    def consistent(var_name, csp):
        """Returns True if the current assignment of the variable VAR_NAME doesn't violate any constraints.
        Assumes that a constraint involving unassigned variables can still be satisfied.
        """
        for constraint in csp.constraints:
            if var_name in constraint.var_names:
                arg_list = [csp.var_dict[name] for name in constraint.var_names]
                if None in arg_list:
                    continue
                if not constraint.satisfied(*arg_list):
                    return False
        return True


    #################
    # MIN CONFLICTS #
    #################

    def min_conflicts(self, take_first=True):
        """Local search / iterative improvement.
        Solves the CSP given by `self.csp`.
        """
        _csp = copy.deepcopy(self.csp)
        # TODO
