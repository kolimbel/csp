from problem import *

def backtracking_search(problem):
    return recursive_backtracking(Solution(), problem)

def recursive_backtracking(assignment, problem):
    if n >= problem.graph