#!/usr/bin/env python

"""
n_queens.py

N-queens solver (`CSPy` usage example).
"""

import itertools
import numpy as np
import matplotlib.pyplot as plt
from cspy import Variable, Constraint, CSP

##############
# PARAMETERS #
##############

N         = 8
VARIABLES = 'pieces'  # either 'squares' or 'pieces'. For efficiency, choose 'pieces'.
PLOT_SOLN = True
ALGORITHM = 'min_conflicts'  # either 'backtracking' or 'min_conflicts'. For efficiency, choose 'min_conflicts'.

# Given an N x N chessboard, can we find a configuration in which to place N queens
# on the board such that no two queens attack each other?

def get_diagonal(r, c, heading='se'):
    """Returns the positions on the diagonal starting at (r, c) as a list of '<row><col>' strings.
    HEADING should be passed in as either 'se' (representing southeast travel) or 'ne'.
    """
    assert heading in {'se', 'ne'}, 'invalid heading direction'
    diagonal = []
    for i in range(N):
        if r < 0 or c < 0 or r >= N or c >= N:
            break
        diagonal.append('%d%d' % (r, c))
        r = r + 1 if heading == 'se' else r - 1
        c += 1
    return diagonal

def from_name(_str):
    """Returns a (r, c) tuple from the '<row><col>' name string _STR."""
    return int(_str) // (10 * (N // 10 + 1)), int(_str) % (10 * (N // 10 + 1))

if __name__ == '__main__':
    csp = CSP()
    var_names = []
    if VARIABLES == 'squares':
        # An illustration of how problem formulation can make all the difference.
        # This setup is much, much less efficient than that of 'pieces'.
        for r in range(N):
            for c in range(N):
                name = '%d%d' % (r, c)
                var_names.append(name)
                csp.add_variable(Variable(name, {0, 1}))
        by_row = [['%d%d' % (r, c) for c in range(N)] for r in range(N)]
        by_col = [['%d%d' % (r, c) for r in range(N)] for c in range(N)]
        by_dia = [get_diagonal(r, 0, 'se') for r in range(N)]
        by_dia.extend([get_diagonal(0, c, 'se') for c in range(N)])
        by_dia.extend([get_diagonal(r, 0, 'ne') for r in range(N)])
        by_dia.extend([get_diagonal(N - 1, c, 'ne') for c in range(N)])
        by_row = map(tuple, by_row)
        by_col = map(tuple, by_col)
        by_dia = set(map(tuple, by_dia))  # remove duplicate diagonals
        for row_positions in by_row:
            for names in itertools.combinations(row_positions, 2):
                csp.add_constraint(Constraint(names, lambda v0, v1: (v0.value, v1.value) != (1, 1)))
        for col_positions in by_col:
            for names in itertools.combinations(col_positions, 2):
                csp.add_constraint(Constraint(names, lambda v0, v1: (v0.value, v1.value) != (1, 1)))
        for dia_positions in by_dia:
            for names in itertools.combinations(dia_positions, 2):
                csp.add_constraint(Constraint(names, lambda v0, v1: (v0.value, v1.value) != (1, 1)))
        csp.add_constraint(Constraint(var_names, lambda *args: sum([v.value for v in args]) == N))
    else:
        for i in range(N):
            var_names.append(str(i))
            csp.add_variable(Variable(str(i), [(r, c) for r in range(N) for c in range(N)]))
        for names in itertools.combinations(var_names, 2):
            csp.add_constraint(Constraint(names, lambda v0, v1: v0.value[0] != v1.value[0]))
            csp.add_constraint(Constraint(names, lambda v0, v1: v0.value[1] != v1.value[1]))
            csp.add_constraint(Constraint(names, lambda v0, v1: abs(v0.value[0] - v1.value[0]) != abs(v0.value[1] - v1.value[1])))
    solution = csp.get_solution(algorithm=ALGORITHM)
    print(solution)
    if PLOT_SOLN and solution is not None:
        board = np.zeros((N, N))
        if VARIABLES == 'squares':
            for name, value in solution.items():
                r, c = from_name(name)
                board[r, c] = value
        else:
            for r, c in solution.values():
                board[r, c] = 1
        plt.imshow(board)
        plt.show()
