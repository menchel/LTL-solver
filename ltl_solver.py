from kripke import *
from LTL import *
from collections import deque

def LTL_solver(formula,structure,source,limit=10):
    """
    Solves an LTL formula
    """
    # singular prop
    if isinstance(formula,Prop):
        name = formula.name
        return name in structure.get_labels(source)
    
    # singular prop
    elif isinstance(formula,Not):
        return not LTL_solver(formula.inner,structure,source,limit)
    
    # and
    elif isinstance(formula,And):
        return LTL_solver(formula.left,structure,source,limit) and LTL_solver(formula.right,structure,source,limit)
    
    # or
    elif isinstance(formula,Or):
        return LTL_solver(formula.left,structure,source,limit) or LTL_solver(formula.right,structure,source,limit)
    
    # next
    elif isinstance(formula,Next):
        if limit <= 0:
            return False
        all_next = structure.get_next(source)
        for next_vert in all_next:
            if LTL_solver(formula.inner, structure, next_vert, limit - 1):
                return True
        return False
    
    # eventually
    elif isinstance(formula, Eventually):
        if limit <= 0:
            return False
        reachable = structure.get_reachable_states(source)
        for vert in reachable:
            if LTL_solver(formula.inner,structure,vert,limit-1):
                return True
        return False

    # always
    elif isinstance(formula, Always):
        if limit <= 0:
            return False
        reachable = structure.get_reachable_states(source)
        for vert in reachable:
            if not LTL_solver(formula.inner,structure,vert,limit-1):
                return False
        return False
    
    # until
    elif isinstance(formula, Until):
        if limit <= 0:
            return False
        visited = set()
        queue = deque([source])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            # bad path
            if not LTL_solver(formula.start, structure, current, limit) and not LTL_solver(formula.end, structure, current, limit):
                continue

            # valid
            if LTL_solver(formula.end, structure, current, limit-1):
                return True

            # continue
            if LTL_solver(formula.start, structure, current,limit-1):
                for succ in structure.get_reachable_states(current):
                    if succ not in visited:
                        queue.append(succ)
        # non found
        return False
