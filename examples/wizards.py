#!/usr/bin/env python

"""
wizards.py

Solver for CS 170's Fall 2017 project.
"""

import argparse
from cspy import Variable, Constraint, CSP
from cspy.common_constraints import uniqueness

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='wizards constraint solver')
    parser.add_argument('input_file', type=str, help='___.in')
    args = parser.parse_args()

    # Read the input file
    with open(args.input_file) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)
    wizards = list(wizards)

    # Initialize domains
    domains = {}  # {wizard: index}
    for wizard in wizards:
        domains[wizard] = set(range(num_wizards))

    # Solve the problem
    csp = CSP()
    for wizard in wizards:
        csp.add_variable(Variable(wizard, domains[wizard]))
    for wiz_a, wiz_b, wiz_c in constraints:
        csp.add_constraint(Constraint((wiz_a, wiz_b, wiz_c), lambda a, b, c: c < min(a, b) or c > max(a, b)))
    for ineq_constraint in uniqueness(wizards, pairwise=True):
        csp.add_constraint(ineq_constraint)
    solution = csp.get_solution(algorithm='backtracking')
    print(sorted(solution, key=solution.get))
