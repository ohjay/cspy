#!/usr/bin/env python

"""
simple.py

Simple example; hardly worth mentioning. Mainly just here for debugging.
"""

from cspy import Variable, Constraint, CSP

if __name__ == '__main__':
    x = Variable('x', {1, 2, 3, 4})
    y = Variable('y', {2, 3, 4, 5})
    z = Variable('z', {3, 4, 5, 6})
    constraint0 = Constraint(('x', 'y'), lambda x, y: x < y)
    constraint1 = Constraint(('x', 'z'), lambda x, z: x > z)
    csp = CSP()
    for var in (x, y, z):
        csp.add_variable(var)
    for constraint in (constraint0, constraint1):
        csp.add_constraint(constraint)
    solution = csp.get_solution(algorithm='backtracking')
    print(solution)  # expect x = 4, y = 5, z = 3
