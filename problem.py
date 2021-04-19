from random_graph import *
from csp_methods import *
import networkx as nx
import matplotlib.pyplot as plt


# class Problem:
#     def __init__(self, graph, vars, domains, constraints):
#         self.graph = graph
#         self.vars = vars
#         self.vars_count = len(vars)
#         self.domains = domains
#         self.constraints = constraints
#
#
# class Constraints:
#     def __init__(self, constraints):
#         self.constraints = constraints
#
#
# class Solution:
#     def __init__(self, vars_count):
#         self.solution = [2] * vars_count
#
#
# class Solutions:
#     def __init__(self):
#         self.solutions = []
#
#     def add_solution(self, solution):
#         self.solutions.insert(len(self.solutions), solution)
#
#     def get_solutions(self):
#         return self.solutions


class Problem:
    def __init__(self, variables, domains, bindings, constraints):
        self.variables = variables
        self.domains = domains
        self.bindings = bindings
        self.constraints = constraints
        self.number_assigned = 0
        self.available_domains = None
        self.visited = 0

    def number_of_conflicts(self, var, val, assignment):
        counter_conflicts = 0

        for v in self.bindings[var]:
            if v in assignment:
                self.visited += 1
                v_val = assignment[v]
                if self.constraints(var, val, v, v_val) is False:
                    counter_conflicts += 1
                    self.visited += 1
                else:
                    self.visited += 1

        return counter_conflicts






