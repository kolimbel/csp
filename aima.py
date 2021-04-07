"""CSP (Constraint Satisfaction Problems) problems and solvers. (Chapter 5)."""

from __future__ import generators

import random
import functools
from filecmp import cmp

from utils import *
import search
import types

def argmin_random_tie(seq, fn):
    """Return an element with lowest fn(seq[i]) score; break ties at random.
    Thus, for all s,f: argmin_random_tie(s, f) in argmin_list(s, f)"""
    best_score = fn(seq[0]); n = 0
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score; n = 1
        elif x_score == best_score:
            n += 1
            if random.randrange(n) == 0:
                    best = x
    return best

def count_if(predicate, seq):
    """Count the number of elements of seq for which the predicate is true.
    >>> count_if(callable, [42, None, max, min])
    2
    """
    f = lambda count, x: count + (not not predicate(x))
    return functools.reduce(f, seq, 0)

def find_if(predicate, seq):
    """If there is an element of seq that satisfies predicate; return it.
    >>> find_if(callable, [3, min, max])
    <built-in function min>
    >>> find_if(callable, [1, 2, 3])
    """
    for x in seq:
        if predicate(x): return x
    return None

def every(predicate, seq):
    """True if every element of seq satisfies predicate.
    >>> every(callable, [min, max])
    1
    >>> every(callable, [min, 3])
    0
    """
    for x in seq:
        if not predicate(x): return False
    return True


class BaseSet:
    "set type (see http://docs.python.org/lib/types-set.html)"

    def __init__(self, elements=[]):
        self.dict = {}
        for e in elements:
            self.dict[e] = 1

    def __len__(self):
        return len(self.dict)

    def __iter__(self):
        for e in self.dict:
            yield e

    def __contains__(self, element):
        return element in self.dict

    def issubset(self, other):
        for e in self.dict.keys():
            if e not in other:
                return False
        return True

    def issuperset(self, other):
        for e in other:
            if e not in self:
                return False
        return True

    def union(self, other):
        return type(self)(list(self) + list(other))

    def intersection(self, other):
        return type(self)([e for e in self.dict if e in other])

    def difference(self, other):
        return type(self)([e for e in self.dict if e not in other])

    def symmetric_difference(self, other):
        return type(self)([e for e in self.dict if e not in other] +
                          [e for e in other if e not in self.dict])

    def copy(self):
        return type(self)(self.dict)

    def __repr__(self):
        elements = ", ".join(map(str, self.dict))
        return "%s([%s])" % (type(self).__name__, elements)

    __le__ = issubset
    __ge__ = issuperset
    __or__ = union
    __and__ = intersection
    __sub__ = difference
    __xor__ = symmetric_difference


class frozenset(BaseSet):
    "A frozenset is a BaseSet that has a hash value and is immutable."

    def __init__(self, elements=[]):
        BaseSet.__init__(elements)
        self.hash = 0
        for e in self:
            self.hash |= hash(e)

    def __hash__(self):
        return self.hash

class set(BaseSet):
    "A set is a BaseSet that does not have a hash, but is mutable."

    def update(self, other):
        for e in other:
            self.add(e)
        return self

    def intersection_update(self, other):
        for e in self.dict.keys():
            if e not in other:
                self.remove(e)
        return self

    def difference_update(self, other):
        for e in self.dict.keys():
            if e in other:
                self.remove(e)
        return self

    def symmetric_difference_update(self, other):
        to_remove1 = [e for e in self.dict if e in other]
        to_remove2 = [e for e in other if e in self.dict]
        self.difference_update(to_remove1)
        self.difference_update(to_remove2)
        return self

    def add(self, element):
        self.dict[element] = 1

    def remove(self, element):
        del self.dict[element]

    def discard(self, element):
        if element in self.dict:
            del self.dict[element]

    def pop(self):
        key, val = self.dict.popitem()
        return key

    def clear(self):
        self.dict.clear()

    __ior__ = update
    __iand__ = intersection_update
    __isub__ = difference_update
    __ixor__ = symmetric_difference_update

class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following three inputs:
        vars        A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases. (For example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(N^4) for the
    explicit representation.) In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP.  Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        succ()                  Return a list of (action, state) pairs
        goal_test(a)            Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
        """

    def __init__(self, vars, domains, neighbors, constraints):
        "Construct a CSP problem. If vars is empty, it becomes domains.keys()."
        vars = vars or domains.keys()
        self.update(self, vars=vars, domains=domains,
               neighbors=neighbors, constraints=constraints,
               initial={}, curr_domains=None, pruned=None, nassigns=0)

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any.
        Do bookkeeping for curr_domains and nassigns."""
        self.nassigns += 1
        assignment[var] = val
        if self.curr_domains:
            if self.fc:
                self.forward_check(var, val, assignment)
            # if self.mac:
            #     AC3(self, [(Xk, var) for Xk in self.neighbors[var]])

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment; that is backtrack.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            # Reset the curr_domain to be the full original domain
            if self.curr_domains:
                self.curr_domains[var] = self.domains[var][:]
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        "Return the number of conflicts var=val has with other variables."
        # Subclasses may implement this more efficiently
        def conflict(var2):
            val2 = assignment.get(var2, None)
            return val2 != None and not self.constraints(var, val, var2, val2)
        return count_if(conflict, self.neighbors[var])

    def forward_check(self, var, val, assignment):
        "Do forward checking (current domain reduction) for this assignment."
        if self.curr_domains:
            # Restore prunings from previous value of var
            for (B, b) in self.pruned[var]:
                self.curr_domains[B].append(b)
            self.pruned[var] = []
            # Prune any other B=b assignement that conflict with var=val
            for B in self.neighbors[var]:
                if B not in assignment:
                    for b in self.curr_domains[B][:]:
                        if not self.constraints(var, val, B, b):
                            self.curr_domains[B].remove(b)
                            self.pruned[var].append((B, b))

    def display(self, assignment):
        "Show a human-readable representation of the CSP."
        # Subclasses can print in a prettier way, or display with a GUI
        print('CSP:', self, 'with assignment:', assignment)

    ## These methods are for the tree and graph search interface:

    def succ(self, assignment):
        "Return a list of (action, state) pairs."
        if len(assignment) == len(self.vars):
            return []
        else:
            var = find_if(lambda v: v not in assignment, self.vars)
            result = []
            for val in self.domains[var]:
                if self.nconflicts(self, var, val, assignment) == 0:
                    a = assignment.copy; a[var] = val
                    result.append(((var, val), a))
            return result

    def goal_test(self, assignment):
        "The goal is to assign all vars, with all constraints satisfied."
        return (len(assignment) == len(self.vars) and
                every(lambda var: self.nconflicts(var, assignment[var],
                                                  assignment) == 0,
                      self.vars))

    ## This is for min_conflicts search

    def conflicted_vars(self, current):
        "Return a list of variables in current assignment that are in conflict"
        return [var for var in self.vars
                if self.nconflicts(var, current[var], current) > 0]

# CSP Backtracking Search

def backtracking_search(csp, mcv=False, lcv=False, fc=False, mac=False):
    """Set up to do recursive backtracking search. Allow the following options:
    mcv - If true, use Most Constrained Variable Heuristic
    lcv - If true, use Least Constraining Value Heuristic
    fc  - If true, use Forward Checking
    mac - If true, use Maintaining Arc Consistency.              [Fig. 5.3]
    >>> backtracking_search(australia)
    {'WA': 'B', 'Q': 'B', 'T': 'B', 'V': 'B', 'SA': 'G', 'NT': 'R', 'NSW': 'R'}
    """
    if fc or mac:
        csp.curr_domains, csp.pruned = {}, {}
        for v in csp.vars:
            csp.curr_domains[v] = csp.domains[v][:]
            csp.pruned[v] = []
    update(csp, mcv=mcv, lcv=lcv, fc=fc, mac=mac)
    return recursive_backtracking({}, csp)

def recursive_backtracking(assignment, csp):
    """Search for a consistent assignment for the csp.
    Each recursive call chooses a variable, and considers values for it."""
    if len(assignment) == len(csp.vars):
        return assignment
    var = select_unassigned_variable(assignment, csp)
    for val in order_domain_values(var, assignment, csp):
        if csp.fc or csp.number_of_conflicts(var, val, assignment) == 0:
            csp.assign(var, val, assignment)
            result = recursive_backtracking(assignment, csp)
            if result is not None:
                return result
        csp.unassign(var, assignment)
    return None

def select_unassigned_variable(assignment, csp):
    "Select the variable to work on next.  Find"
    if csp.mcv: # Most Constrained Variable
        unassigned = [v for v in csp.vars if v not in assignment]
        return argmin_random_tie(unassigned,
                     lambda var: -num_legal_values(csp, var, assignment))
    else: # First unassigned variable
        for v in csp.vars:
            if v not in assignment:
                return v

def order_domain_values(var, assignment, csp):
    "Decide what order to consider the domain variables."
    if csp.curr_domains:
        domain = csp.curr_domains[var]
    else:
        domain = csp.domains[var][:]
    if csp.lcv:
        # If LCV is specified, consider values with fewer conflicts first
        key = lambda val: csp.number_of_conflicts(var, val, assignment)
        domain.sort(lambda x_y: cmp(key(x_y[0]), key(x_y[1])))
    while domain:
        yield domain.pop()

def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count_if(lambda val: csp.number_of_conflicts(var, val, assignment) == 0,
                        csp.domains[var])


australia_map = Graph(dict(
    T=dict(),
    SA=dict(WA=1, NT=1, Q=1, NSW=1, V=1),
    NT=dict(WA=1, Q=1),
    NSW=dict(Q=1, V=1)))
australia_map.locations = dict(WA=(120, 24), NT=(135, 20), SA=(135, 30),
                               Q=(145, 20), NSW=(145, 32), T=(145, 42),
                               V=(145, 37))