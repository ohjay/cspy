#!/usr/bin/env python

"""
sudoku.py

Sudoku solver (`CSPy` usage example).
Solves https://github.com/ohjay/cspy/blob/master/examples/sudoku.png.

From testing different Sudoku formulations, a tip for problem setup:
avoid many-variable constraints. Keep things pairwise if possible.
"""

from cspy import Variable, Constraint, CSP
from cspy.utils import merge_dicts
from cspy.common_constraints import uniqueness, inequality_unary

N = 9
DOMAIN = tuple(range(1, N + 1))
FIXED_VALUES = {
    (0, 0): 5, (0, 1): 3, (0, 4): 7,
    (1, 0): 6, (1, 3): 1, (1, 4): 9, (1, 5): 5,
    (2, 1): 9, (2, 2): 8, (2, 7): 6,
    (3, 0): 8, (3, 4): 6, (3, 8): 3,
    (4, 0): 4, (4, 3): 8, (4, 5): 3, (4, 8): 1,
    (5, 0): 7, (5, 4): 2, (5, 8): 6,
    (6, 1): 6, (6, 6): 2, (6, 7): 8,
    (7, 3): 4, (7, 4): 1, (7, 5): 9, (7, 8): 5,
    (8, 4): 8, (8, 7): 7, (8, 8): 9
}

def contains_all(iterable):
    """Returns True if the given iterable contains all of the digits from 1 through N."""
    return all(d in iterable for d in DOMAIN)

def values(var_list):
    """Takes in a list of variables and returns a list of those variables' values."""
    return [v.value for v in var_list]

def from_name(_str):
    """Returns a (r, c) tuple from the '<row><col>' name string _STR."""
    return int(_str) // (10 * (N // 10 + 1)), int(_str) % (10 * (N // 10 + 1))

def print_grid(known_values, unknown_char='-'):
    """Given a dictionary of known values, prints the grid."""
    for r in range(N):
        rowstr = ''
        for c in range(N):
            rowstr += str(known_values.get((r, c), unknown_char)) + ' '
        print(rowstr)

if __name__ == '__main__':
    print('Solving this problem:')
    print_grid(FIXED_VALUES)
    csp = CSP()
    for r in range(N):
        for c in range(N):
            if (r, c) not in FIXED_VALUES:
                csp.add_variable(Variable('%d%d' % (r, c), set(DOMAIN)))
    by_row = [['%d%d' % (r, c) for c in range(N) if (r, c) not in FIXED_VALUES] for r in range(N)]
    by_row = [(_, [val for rc, val in FIXED_VALUES.items() if rc[0] == r]) for r, _ in enumerate(by_row)]
    by_col = [['%d%d' % (r, c) for r in range(N) if (r, c) not in FIXED_VALUES] for c in range(N)]
    by_col = [(_, [val for rc, val in FIXED_VALUES.items() if rc[1] == c]) for c, _ in enumerate(by_col)]
    by_box = []
    for r in range(0, N, 3):
        for c in range(0, N, 3):
            box, fixed = [], []
            for i in range(3):
                for j in range(3):
                    val = FIXED_VALUES.get((r + i, c + j), None)
                    if val is None:
                        box.append('%d%d' % (r + i, c + j))
                    else:
                        fixed.append(val)
            by_box.append((box, fixed))
    for row_positions, fixed in by_row:
        for ineq_constraint in uniqueness(row_positions, pairwise=True):
            csp.add_constraint(ineq_constraint)
        for name in row_positions:
            for val in fixed:
                csp.add_constraint(inequality_unary(name, val))
    for col_positions, fixed in by_col:
        for ineq_constraint in uniqueness(col_positions, pairwise=True):
            csp.add_constraint(ineq_constraint)
        for name in col_positions:
            for val in fixed:
                csp.add_constraint(inequality_unary(name, val))
    for box_positions, fixed in by_box:
        for ineq_constraint in uniqueness(box_positions, pairwise=True):
            csp.add_constraint(ineq_constraint)
        for name in box_positions:
            for val in fixed:
                csp.add_constraint(inequality_unary(name, val))
    solution = csp.get_solution(algorithm='backtracking')
    if solution is None:
        solution = {}
    _solution = {from_name(k): v for k, v in solution.items()}
    print_grid(merge_dicts(_solution, FIXED_VALUES))
