#!/usr/bin/env python

"""
sudoku.py

Basic Sudoku example (solves a 6x6 grid).
Solves https://upload.wikimedia.org/wikipedia/commons/0/08/Sudoku6x6-sol2.png.
"""

import numpy as np
from cspy import Variable, Constraint, CSP

N = 6
DOMAIN = tuple(range(1, N + 1))
FIXED_VALUES = {
    (0, 0): 2, (0, 5): 3,
    (1, 1): 1, (1, 3): 2, (1, 5): 4,
    (2, 0): 1, (2, 3): 3,
    (3, 2): 6, (3, 5): 1,
    (4, 0): 4, (4, 2): 1, (4, 4): 3,
    (5, 0): 3, (5, 5): 2,
}

def contains_all(iterable):
    """Returns True if the given iterable contains all of the digits from 1 through N.
    >>> contains_all([1, 2, 3, 4, 5, 6])
    True
    >>> contains_all([2, 6, 4, 5, 1, 3])
    True
    >>> contains_all([2, 6, 4, 5, 1])
    False
    >>> contains_all([3, 5, 2, 4, 0, 1])
    False
    """
    return all(d in iterable for d in DOMAIN)

def values(var_list):
    """Takes in a list of variables and returns a list of those variables' values."""
    return [v.value for v in var_list]

if __name__ == '__main__':
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
    for r in range(0, N, 2):
        for c in range(0, N, 3):
            box, fixed = [], []
            for i in range(2):
                for j in range(3):
                    val = FIXED_VALUES.get((r + i, c + j), None)
                    if val is None:
                        box.append('%d%d' % (r + i, c + j))
                    else:
                        fixed.append(val)
            by_box.append((box, fixed))
    for row_positions, fixed in by_row:
        satisfied = (lambda fixed: lambda *args: contains_all(fixed + values(args)))(fixed)
        csp.add_constraint(Constraint(row_positions, satisfied))
    for col_positions, fixed in by_col:
        satisfied = (lambda fixed: lambda *args: contains_all(fixed + values(args)))(fixed)
        csp.add_constraint(Constraint(col_positions, satisfied))
    for box_positions, fixed in by_box:
        satisfied = (lambda fixed: lambda *args: contains_all(fixed + values(args)))(fixed)
        csp.add_constraint(Constraint(box_positions, satisfied))
    solution = csp.get_solution(algorithm='backtracking')
    if solution is None:
        print(solution)
    else:
        grid = np.zeros((N, N))
        for r in range(N):
            for c in range(N):
                if (r, c) in FIXED_VALUES:
                    grid[r, c] = FIXED_VALUES[(r, c)]
                else:
                    grid[r, c] = solution['%d%d' % (r, c)]
        print(grid)
