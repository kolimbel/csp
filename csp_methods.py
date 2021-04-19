import random


def recursive_backtracking(assignment, csp, fc, fst_domain, mrv):
    if len(assignment) == len(csp.variables):
        return assignment

    if mrv is True:
        #raise Exception('') #TODO zaimplementować
        var = mrv_f(assignment, csp)
    else:
        var = select_unassigned_variable(assignment, csp)

    # if fst_domain:
    #     pass
    # else:
    #     raise Exception('brak innej heurystyki dla wyboru wartosci z domeny')

    for val in order_domain_values(var, csp):
        if csp.number_of_conflicts(var, val, assignment) == 0:

            # assign
            assignment[var] = val
            csp.number_assigned += 1

            if fc:
                if csp.available_domains is None:
                    csp.available_domains = {v: list(csp.domains[v]) for v in csp.variables}
                    #csp.visited += len(csp.variables)

                excluded = [(var, a) for a in csp.available_domains[var] if a != val]
                csp.available_domains[var] = [val]

                forward_checking(csp, var, val, assignment, excluded)
                result = recursive_backtracking(assignment, csp, fc, fst_domain, mrv)
                if result is not None:
                    return result
            # if fc:
            #
            #     excluded = [(var, a) for a in csp.available_domains[var] if a != val]
            #     csp.available_domains[var] = [val]
            #
            #     forward_checking(csp, var, val, assignment, excluded)
            #     result = recursive_backtracking(assignment, csp, fc, fst_domain, mrv)
            #     if result is not None:
            #         return result
            else:
                result = recursive_backtracking(assignment, csp, fc, fst_domain, mrv)
                if result is not None:
                    return result

        # unassign
        if var in assignment:
            del assignment[var]

    return None


def backtracking_search(csp, fc, fst_domain, mrv):
    return recursive_backtracking({}, csp, fc, fst_domain, mrv)


def forward_checking(csp, var, value, assignment, excluded):
    if csp.available_domains is None:
        csp.available_domains = {v: list(csp.domains[v]) for v in csp.variables}
        #csp.visited += len(csp.variables)

    for var_bind in csp.bindings[var]:
        if var_bind not in assignment:
            for val_bind in csp.available_domains[var_bind][:]:
                if not csp.constraints(var, value, var_bind, val_bind):
                    #csp.visited += 1
                    # wykluczyć rozpatrywany
                    csp.available_domains[var_bind].remove(val_bind)
                    if excluded is not None:
                        excluded.append((var_bind, val_bind))
                #else:
                    #csp.visited += 1


# kolejnosc zmiennej
def select_unassigned_variable(assignment, csp):
    for var in csp.variables:
        #csp.visited += 1
        if var in assignment:
            #csp.visited += 1
            pass
        else:
            #csp.visited += 1
            return var


#
identity = lambda x: x


def argmin_random_tie(seq, key=identity):
    """Return a minimum element of seq; break ties at random."""
    shuffled_items = shuffled(seq)
    result = min(shuffled_items, key=key)
    #return min(shuffled(seq), key=key)
    return result


def shuffled(iterable):
    """Randomly shuffle a copy of iterable."""
    items = list(iterable)
    random.shuffle(items)
    return items

def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(map(bool, seq))

#


def mrv_f(assignment, csp):
    """Minimum-remaining-values heuristic."""
    available_variables = [v for v in csp.variables if v not in assignment]
    csp.visited += len(csp.variables)
    #csp.visited += len(assignment)
    keyk = lambda var: num_legal_values(csp, var, assignment)
    result = argmin_random_tie(available_variables, keyk)
    return result


def num_legal_values(csp, var, assignment):
    if csp.available_domains:
        return len(csp.available_domains[var])
    else:
        return count(csp.number_of_conflicts(var, val, assignment) == 0 for val in csp.domains[var])


# kolejnosc wartosci z dziedzin
def order_domain_values(var, csp):
    try:
        temp_domain = csp.available_domains[var]
    except:
        temp_domain = csp.domains[var][:]
    while len(temp_domain) > 0:
        val = temp_domain[len(temp_domain) - 1]
        temp_domain.remove(val)
        yield val