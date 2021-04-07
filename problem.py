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
from collections import defaultdict

from random_graph import *


# class Problem:
#     """The abstract class for a formal problem. You should subclass
#     this and implement the methods actions and result, and possibly
#     __init__, goal_test, and path_cost. Then you will create instances
#     of your subclass and solve them with the various search functions."""
#
#     def __init__(self, initial, goal=None):
#         """The constructor specifies the initial state, and possibly a goal
#         state, if there is a unique goal. Your subclass's constructor can add
#         other arguments."""
#         self.initial = initial
#         self.goal = goal
#
#     def actions(self, state):
#         """Return the actions that can be executed in the given
#         state. The result would typically be a list, but if there are
#         many actions, consider yielding them one at a time in an
#         iterator, rather than building them all at once."""
#         raise NotImplementedError
#
#     def result(self, state, action):
#         """Return the state that results from executing the given
#         action in the given state. The action must be one of
#         self.actions(state)."""
#         raise NotImplementedError
#
#     def goal_test(self, state):
#         """Return True if the state is a goal. The default method compares the
#         state to self.goal or checks for state in self.goal if it is a
#         list, as specified in the constructor. Override this method if
#         checking against a single self.goal is not enough."""
#         if isinstance(self.goal, list):
#             return is_in(state, self.goal)
#         else:
#             return state == self.goal
#
#     def path_cost(self, c, state1, action, state2):
#         """Return the cost of a solution path that arrives at state2 from
#         state1 via action, assuming cost c to get up to state1. If the problem
#         is such that the path doesn't matter, this function will only look at
#         state2. If the path does matter, it will consider c and maybe state1
#         and action. The default method costs 1 for every step in the path."""
#         return c + 1
#
#     def value(self, state):
#         """For optimization problems, each state has a value. Hill Climbing
#         and related algorithms try to maximize this value."""
#         raise NotImplementedError

class CSP():
    """This class describes finite-domain Constraint Satisfaction Problems.
        A CSP is specified by the following inputs:
            variables   A list of variables; each is atomic (e.g. int or string).
            domains     A dict of {var:[possible_value, ...]} entries.
            neighbors   A dict of {var:[var,...]} that for each variable lists
                        the other variables that participate in constraints.
            constraints A function f(A, a, B, b) that returns true if neighbors
                        A, B satisfy the constraint when they have values A=a, B=b
        In the textbook and in most mathematical definitions, the
        constraints are specified as explicit pairs of allowable values,
        but the formulation here is easier to express and more compact for
        most cases (for example, the n-Queens problem can be represented
        in O(n) space using this notation, instead of O(n^4) for the
        explicit representation). In terms of describing the CSP as a
        problem, that's all there is.
        However, the class also supports data structures and methods that help you
        solve CSPs by calling a search function on the CSP. Methods and slots are
        as follows, where the argument 'a' represents an assignment, which is a
        dict of {var:val} entries:
            assign(var, val, a)     Assign a[var] = val; do other bookkeeping
            unassign(var, a)        Do del a[var], plus other bookkeeping
            nconflicts(var, val, a) Return the number of other variables that
                                    conflict with var=val
            curr_domains[var]       Slot: remaining consistent values for var
                                    Used by constraint propagation routines.
        The following methods are used only by graph_search and tree_search:
            actions(state)          Return a list of actions
            result(state, action)   Return a successor of state
            goal_test(state)        Return true if all constraints satisfied
        The following are just for debugging purposes:
            nassigns                Slot: tracks the number of assignments made
            display(a)              Print a human-readable representation
        """

    def __init__(self, variables, domains, neighbors, constraints):
        #super().__init__(())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0



    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

        # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

def first(iterable, default=None):
    """Return the first element of an iterable; or default."""
    return next(iter(iterable), default)

def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(map(bool, seq))

def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)

def select_unassigned_variable(assignment, csp):
    "Select the variable to work on next.  Find"
    for v in csp.variables:
        if v not in assignment:
            return v

def order_domain_values(var, assignment, csp):
    "Decide what order to consider the domain variables."
    if csp.curr_domains:
        domain = csp.curr_domains[var]
    else:
        domain = csp.domains[var][:]
    while domain:
        yield domain.pop()

def recursive_backtracking(assignment, csp, fc):
    if len(assignment) == len(csp.variables):
        return assignment
    var = select_unassigned_variable(assignment, csp)
    for val in order_domain_values(var, assignment, csp):
        if csp.nconflicts(var, val, assignment) == 0:

            # assign
            assignment[var] = val
            csp.nassigns += 1
            #

            if fc:
                removals = csp.suppose(var, val)
                forward_checking(csp, var, val, assignment, removals)
                result = recursive_backtracking(assignment, csp, fc)
                if result is not None:
                    return result
            else:
                result = recursive_backtracking(assignment, csp, fc)
                if result is not None:
                    return result

        # unassign
        if var in assignment:
            del assignment[var]
        #

    return None

# def recursive_backtracking(assignment, csp, fc):
#     if len(assignment) == len(csp.variables):
#         return assignment
#     var = select_unassigned_variable(assignment, csp)
#     for val in order_domain_values(var, assignment, csp):
#         if csp.nconflicts(var, val, assignment) == 0:
#             csp.assign(var, val, assignment)
#             result = recursive_backtracking(assignment, csp)
#             if result is not None:
#                 return result
#         csp.unassign(var, assignment)
#     return None


def backtracking_search(csp, fc=False):
    return recursive_backtracking({}, csp, fc)


def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True


# ______________________________________________________________________________
# Map Coloring CSP Problems


class UniversalDict:
    """A universal dict maps any key to the same value. We use it here
    as the domains dict for CSPs in which all variables have the same domain.
    >> d = UniversalDict(42)
    >> d['life']
    42
    """

    def __init__(self, value):
        self.value = value
        costam = 5

    def __getitem__(self, key): return self.value

    def __repr__(self): return '{{Any: {0!r}}}'.format(self.value)


def different_values_constraint(A, a, B, b):
    """A constraint saying two neighboring variables must differ in value."""
    return a != b


def MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    lnk = list(neighbors.keys())
    return CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint)


def parse_neighbors(neighbors):
    """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
    regions to neighbors. The syntax is a region name followed by a ':'
    followed by zero or more region names, followed by ';', repeated for
    each region name. If you say 'X: Y' you don't need 'Y: X'.
    >>> parse_neighbors('X: Y Z; Y: Z') == {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
    True
    """
    dic = defaultdict(list)
    specs = [spec.split(':') for spec in neighbors.split(';')]
    for (A, Aneighbors) in specs:
        A = A.strip()
        for B in Aneighbors.split():
            dic[A].append(B)
            dic[B].append(A)
    return dic

# MAP ZADANIE
#
# australia_csp = MapColoringCSP(list('RGB'), """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)
# australia_csp = MapColoringCSP(['Red', 'Green', 'Blue'], """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)
gr = Graph(30, 30, 10)
australia_csp = MapColoringCSP(['tomato', 'limegreen', 'lightskyblue', 'yellow'], gr.strgraph)
print(australia_csp)
australia_bt = backtracking_search(australia_csp, fc=True)
print(australia_bt)

if australia_bt is None:
    raise Exception('nie znaleziono rozwiąznia') # TODO: zamiast tego ponowic dla nowego grafu i zapisac info o braku rozwiazania

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph(directed=True)
nodes, positions = gr.get_nodes()
for i in range(len(nodes)):
    G.add_node(nodes[i], pos=positions[i])
G.add_edges_from(gr.get_tuples())


black_edges = [edge for edge in G.edges()]

color_map = []
pos_map = []
for node in G:
    try:
        color = australia_bt[str(node)]
    except:
        raise Exception('bledny kolor {}'.format([node, str(node)]))
    color_map.append(color)
    # coordinates = node.split('-')
    # pos_map.append((coordinates[0], coordinates[1]))

# arrows options
options = {
    'node_size': 500,
    'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 10,
}

# Need to create a layout when doing
# separate calls to draw nodes and edges
#pos = nx.spring_layout(G)
#pos = nx.get_node_attributes()
#nx.set_node_attributes(G, pos, 'coord')
pos = nx.get_node_attributes(G, 'pos')
nx.draw_networkx_nodes(G, pos, node_color=color_map, arrows=True, **options, cmap=plt.get_cmap('jet'))
nx.draw_networkx_labels(G, pos, font_size=8)
# nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
# nx.draw_networkx_edges(G, pos, edgelist=green_edges, edge_color='g', arrows=True)
# nx.draw_networkx_edges(G, pos, edgelist=blue_edges, edge_color='b', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
plt.show(block=False)
# plt.close('all')

# KONIEC MAP ZADANIE

def Zebra():
    """Return an instance of the Zebra Puzzle."""
    Colors = 'bialy czerwony niebieski zielony zolty'.split()
    Pets = 'konie koty psy ptaki rybki'.split()
    Drinks = 'herbata kawa mleko piwo woda'.split()
    Countries = 'anglik dunczyk niemiec norweg szwed'.split()
    Smokes = 'cygara fajka bfiltra light mentolowe'.split()
    variables = Colors + Pets + Drinks + Countries + Smokes
    domains = {}
    for var in variables:
        domains[var] = list(range(1, 6))
    domains['norweg'] = [1]  # 1. Norweg zamieszkuje pierwszy dom
    domains['mleko'] = [3]  # 8. Mieszkaniec środkowego domu pija mleko.
    neighbors = parse_neighbors("""anglik: czerwony; zielony: bialy; light: koty; light: woda; norweg: niebieski; konie: zolty;
                niemiec: fajka; bfiltra: ptaki; szwed: psy; zolty: cygara;
                dunczyk: herbata; mentolowe: piwo; zielony: kawa""")
    for type in [Colors, Pets, Drinks, Countries, Smokes]:
        for A in type:
            for B in type:
                if A != B:
                    if B not in neighbors[A]:
                        neighbors[A].append(B)
                    if A not in neighbors[B]:
                        neighbors[B].append(A)

    def zebra_constraint(A, a, B, b, recurse=0):
        same = (a == b)
        next_to = abs(a - b) == 1
        if A == 'anglik' and B == 'czerwony':  # 2
            return same
        if A == 'bialy' and B == 'zielony':  # 3
            return a - 1 == b
        if A == 'dunczyk' and B == 'herbata':  # 4
            return same
        if A == 'light' and B == 'koty':  # 5
            return next_to
        if A == 'zolty' and B == 'cygara':  # 6
            return same
        if A == 'niemiec' and B == 'fajka':  # 7
            return same
        if A == 'light' and B == 'woda':  # 8
            return next_to
        if A == 'bfiltra' and B == 'ptaki':  # 10
            return same
        if A == 'szwed' and B == 'psy':  # 11
            return same
        if A == 'norweg' and B == 'niebieski':  # 12
            return next_to
        if A == 'zolty' and B == 'konie':  # 13
            return next_to
        if A == 'mentolowe' and B == 'piwo':  # 14
            return same
        if A == 'zielony' and B == 'kawa':  # 15
            return same
        if recurse == 0:
            return zebra_constraint(B, b, A, a, 1)
        if ((A in Colors and B in Colors) or
                (A in Pets and B in Pets) or
                (A in Drinks and B in Drinks) or
                (A in Countries and B in Countries) or
                (A in Smokes and B in Smokes)):
            return not same
        raise Exception('error')

    def zebra_constraint2(A, a, B, b):
        # same = (a == b)
        # next_to = abs(a - b) == 1
        variables = set([])
        variables.add(A)
        variables.add(B)

        def contains(val1, val2):
            return variables.__contains__(val1) and variables.__contains__(val2)

        if contains('anglik', 'czerwony'):  # 2. Anglik mieszka w czerwonym domu.
            return a == b
        if contains('bialy', 'zielony'):  # 3. Zielony dom znajduje się bezpośrednio po lewej stronie domu białego.
            return a - 1 == b or a + 1 == b
        if contains('dunczyk', 'herbata'):  # 4. Duńczyk pija herbatkę.
            return a == b
        if contains('light', 'koty'):  # 5. Palacz papierosów light mieszka obok hodowcy kotów.
            return abs(a - b) == 1
        if contains('zolty', 'cygara'):  # 6. Mieszkaniec żółtego domu pali cygara.
            return a == b
        if contains('niemiec', 'fajka'):  # 7. Niemiec pali fajkę.
            return a == b
        if contains('light', 'woda'):  # 9. Palacz papierosów light ma sąsiada, który pija wodę.
            return abs(a - b) == 1
        if contains('bfiltra', 'ptaki'):  # 10. Palacz papierosów bez filtra hoduje ptaki.
            return a == b
        if contains('szwed', 'psy'):  # 11. Szwed hoduje psy.
            return a == b
        if contains('norweg', 'niebieski'):  # 12. Norweg mieszka obok niebieskiego domu.
            return abs(a - b) == 1
        if contains('zolty', 'konie'):  # 13. Hodowca koni mieszka obok żółtego domu.
            return abs(a - b) == 1
        if contains('mentolowe', 'piwo'):  # 14. Palacz mentolowych pija piwo.
            return a == b
        if contains('zielony', 'kawa'):  # 15. W zielonym domu pija się kawę.
            return a == b
        if ((A in Colors and B in Colors) or
                (A in Pets and B in Pets) or
                (A in Drinks and B in Drinks) or
                (A in Countries and B in Countries) or
                (A in Smokes and B in Smokes)):
            return not (a == b)
        #raise Exception('error')

    return CSP(variables, domains, neighbors, zebra_constraint2)

z = Zebra()
print(z)
z_bt = backtracking_search(z, fc=False)
z_bt_s = sorted(z_bt.items(), key=lambda item: item[1])
print(z_bt_s)
print('rybki: ' + str(z_bt['rybki']))

plt.show(block=True)