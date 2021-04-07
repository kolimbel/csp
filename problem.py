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


from random_graph import *


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
            number_of_conflicts(var, val, a) Return the number of other variables that
                                    conflict with var=val
            available_domains[var]       Slot: remaining consistent values for var
                                    Used by constraint propagation routines.
        The following methods are used only by graph_search and tree_search:
            actions(state)          Return a list of actions
            result(state, action)   Return a successor of state
            goal_test(state)        Return true if all constraints satisfied
        The following are just for debugging purposes:
            nassigns                Slot: tracks the number of assignments made
            display(a)              Print a human-readable representation
        """

    def __init__(self, variables, domains, bindings, constraints):
        self.variables = variables
        self.domains = domains
        self.bindings = bindings
        self.constraints = constraints
        self.available_domains = None
        self.nassigns = 0


    def number_of_conflicts(self, var, val, assignment):
        counter_conflicts = 0

        for v in self.bindings[var]:
            if v in assignment:
                v_val = assignment[v]
                if self.constraints(var, val, v, v_val) is False:
                    counter_conflicts += 1

        return counter_conflicts


# kolejnosc zmiennej

def select_unassigned_variable(assignment, csp):
    "Select the variable to work on next.  Find"
    for v in csp.variables:
        if v in assignment:
            pass
        else:
            return v

def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    """Return a minimum element of seq; break ties at random."""
    return min(shuffled([v for v in csp.variables if v not in assignment]),
                             key=lambda var: num_legal_values(csp, var, assignment))

def shuffled(iterable):
    """Randomly shuffle a copy of iterable."""
    items = list(iterable)
    random.shuffle(items)
    return items

def num_legal_values(csp, var, assignment):
    if csp.available_domains:
        return len(csp.available_domains[var])
    else:
        return count(csp.number_of_conflicts(var, val, assignment) == 0 for val in csp.domains[var])

def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(map(bool, seq))

# kolejnosc wartosci z dziedzin

def order_domain_values(var, csp):
    try:
        temp_domain = csp.available_domains[var]
    except:
        temp_domain = csp.domains[var][:]
    while len(temp_domain) > 0:
        val = temp_domain[len(temp_domain)-1]
        temp_domain.remove(val)
        yield val

def recursive_backtracking(assignment, csp, fc, fst_domain):
    if len(assignment) == len(csp.variables):
        return assignment
    var = select_unassigned_variable(assignment, csp)

    if fst_domain:
        pass
    else:
        raise Exception('brak innej heurystyki dla wyboru wartosci z domeny')

    for val in order_domain_values(var, csp):
        if csp.number_of_conflicts(var, val, assignment) == 0:

            # assign
            assignment[var] = val
            csp.nassigns += 1
            #

            if fc:
                """Start accumulating inferences from assuming var=value."""

                """Make sure we can prune values from domains. (We want to pay
                           for this only if we use it.)"""
                if csp.available_domains is None:
                    csp.available_domains = {v: list(csp.domains[v]) for v in csp.variables}

                excluded = [(var, a) for a in csp.available_domains[var] if a != val]
                csp.available_domains[var] = [val]

                forward_checking(csp, var, val, assignment, excluded)
                result = recursive_backtracking(assignment, csp, fc, fst_domain)
                if result is not None:
                    return result
            else:
                result = recursive_backtracking(assignment, csp, fc, fst_domain)
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
#         if csp.number_of_conflicts(var, val, assignment) == 0:
#             csp.assign(var, val, assignment)
#             result = recursive_backtracking(assignment, csp)
#             if result is not None:
#                 return result
#         csp.unassign(var, assignment)
#     return None


def backtracking_search(csp, fc=False, fst_domain=True):
    return recursive_backtracking({}, csp, fc, fst_domain)


def forward_checking(csp, var, value, assignment, excluded):
    """Prune neighbor values inconsistent with var=value."""

    """Make sure we can prune values from domains. (We want to pay
            for this only if we use it.)"""
    if csp.available_domains is None:
        csp.available_domains = {v: list(csp.domains[v]) for v in csp.variables}

    for B in csp.bindings[var]:
        if B not in assignment:
            for b in csp.available_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    """Rule out var=value."""
                    csp.available_domains[B].remove(b)
                    if excluded is not None:
                        excluded.append((B, b))
            if not csp.available_domains[B]:
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

    def __getitem__(self, key): return self.value

    def __repr__(self): return '{{Any: {0!r}}}'.format(self.value)


def different_values_constraint(A, a, B, b):
    """A constraint saying two neighboring variables must differ in value."""
    return a != b


def MapColoringCSP(colors, borders):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(borders, str):
        borders = parse_borders(borders)
    lnk = list(borders.keys())
    return CSP(list(borders.keys()), UniversalDict(colors), borders, different_values_constraint)


def parse_borders(neighbors):
    """Convert a string of the form 'X: Y Z; Y: Z' into a dict mapping
    regions to neighbors. The syntax is a region name followed by a ':'
    followed by zero or more region names, followed by ';', repeated for
    each region name. If you say 'X: Y' you don't need 'Y: X'.
    >>> parse_borders('X: Y Z; Y: Z') == {'Y': ['X', 'Z'], 'X': ['Y', 'Z'], 'Z': ['X', 'Y']}
    True
    """
    #dic = defaultdict(list)
    dic = {}
    specs = [spec.split(':') for spec in neighbors.split(';')]
    for (A, Aneighbors) in specs:
        A = A.strip()
        for B in Aneighbors.split():
            try:
                dic[A].append(B)
            except:
                dic[A] = []
                dic[A].append(B)

            try:
                dic[B].append(A)
            except:
                dic[B] = []
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

def einsteins_puzzle():
    nationality = ['anglik', 'dunczyk', 'niemiec', 'norweg', 'szwed']
    color = ['bialy', 'czerwony', 'niebieski', 'zielony', 'zolty']
    drink = ['herbata', 'kawa', 'mleko', 'piwo', 'woda']
    tobacco = ['cygara', 'fajka', 'bfiltra', 'light', 'mentolowe']
    animal = ['konie', 'koty', 'psy', 'ptaki', 'rybki']
    #variables = [*color, *animal, *drink, *nationality, *tobacco]
    variables = [*nationality, *color, *drink, *tobacco, *animal]
    domains = {}
    for var in variables:
        domains[var] = list(range(1, 6))
    domains['norweg'] = [1]  # 1. Norweg zamieszkuje pierwszy dom
    domains['mleko'] = [3]  # 8. Mieszkaniec środkowego domu pija mleko.
    bindings = parse_borders("""anglik: czerwony; zielony: bialy; light: koty; light: woda; norweg: niebieski; konie: zolty;
                niemiec: fajka; bfiltra: ptaki; szwed: psy; zolty: cygara;
                dunczyk: herbata; mentolowe: piwo; zielony: kawa""")
    for type in [nationality, color, drink, tobacco, animal]:#[color, animal, drink, nationality, tobacco]:
        for fst_var in type:
            for snd_var in type:
                if fst_var != snd_var:
                    if snd_var not in bindings[fst_var]:
                        bindings[fst_var].append(snd_var)
                    try:
                        if fst_var not in bindings[snd_var]:
                            bindings[snd_var].append(fst_var)
                    except:
                        bindings[snd_var] = []
                        if fst_var not in bindings[snd_var]:
                            bindings[snd_var].append(fst_var)


    def ep_constraints(A, a, B, b):
        vars_const = set([])
        vars_const.add(A)
        vars_const.add(B)

        def contains(val1, val2):
            return vars_const.__contains__(val1) and vars_const.__contains__(val2)

        if contains('anglik', 'czerwony'):  # 2. Anglik mieszka w czerwonym domu.
            return a == b
        if contains('bialy', 'zielony'):  # 3. Zielony dom znajduje się bezpośrednio po lewej stronie domu białego.
            return a + 1 == b #a - 1 == b  or
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
        if ((A in color and B in color) or
                (A in animal and B in animal) or
                (A in drink and B in drink) or
                (A in nationality and B in nationality) or
                (A in tobacco and B in tobacco)):
            return not (a == b)

    return CSP(variables, domains, bindings, ep_constraints)

z = einsteins_puzzle()
print(z)
z_bt = backtracking_search(z, fc=False)
z_bt_s = sorted(z_bt.items(), key=lambda item: item[1])
print(z_bt_s)
print('rybki: ' + str(z_bt['rybki']))

plt.show(block=True)