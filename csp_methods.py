import random


def recursive_backtracking(assignment, csp, fc, fst_domain, mrv):
    if len(assignment) == len(csp.variables):
        return assignment

    if mrv is True:
        raise Exception('') #TODO zaimplementować
        #var = mrv(...)
    else:
        var = select_unassigned_variable(assignment, csp)

    if fst_domain:
        pass
    else:
        raise Exception('brak innej heurystyki dla wyboru wartosci z domeny')

    for val in order_domain_values(var, csp):
        if csp.number_of_conflicts(var, val, assignment) == 0:

            # assign
            assignment[var] = val
            csp.number_assigned += 1

            if fc:
                if csp.available_domains is None:
                    csp.available_domains = {v: list(csp.domains[v]) for v in csp.variables}

                excluded = [(var, a) for a in csp.available_domains[var] if a != val]
                csp.available_domains[var] = [val]

                forward_checking(csp, var, val, assignment, excluded)
                result = recursive_backtracking(assignment, csp, fc, fst_domain, mrv)
                if result is not None:
                    return result
            else:
                result = recursive_backtracking(assignment, csp, fc, fst_domain, mrv)
                if result is not None:
                    return result

        # unassign
        if var in assignment:
            del assignment[var]

    return None


def backtracking_search(csp, fc=False, fst_domain=True, mrv=False):
    return recursive_backtracking({}, csp, fc, fst_domain, mrv)


def forward_checking(csp, var, value, assignment, excluded):
    if csp.available_domains is None:
        csp.available_domains = {v: list(csp.domains[v]) for v in csp.variables}

    for B in csp.bindings[var]:
        if B not in assignment:
            for b in csp.available_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    # wykluczyć rozpatrywany
                    csp.available_domains[B].remove(b)
                    if excluded is not None:
                        excluded.append((B, b))
            if not csp.available_domains[B]:
                return False
    return True


# kolejnosc zmiennej
def select_unassigned_variable(assignment, csp):
    for v in csp.variables:
        if v in assignment:
            pass
        else:
            return v


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