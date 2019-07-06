import random
from graph import calc_objective


def k_swap(graph, removed, k=1):
    removed = removed[:]
    k = k if k < len(removed) else len(removed)
    # k rimossi e k non rimossi si scambiano
    left = [node for node in range(len(graph)) if node not in removed]
    for i in range(k):
        swapped_removed_idx = random.randint(0, len(removed) - 1 - i)
        swapped_left_idx = random.randint(0, len(left) - 1 - i)

        swapped_removed = removed.pop(swapped_removed_idx)
        swapped_left = left.pop(swapped_left_idx)
        
        removed.append(swapped_left)
        left.append(swapped_removed)

    return removed


def tabu_search(graph, removed, n_tabu=None, n_stall=100):
    removed = removed[:]

    if n_tabu is None:
        n_tabu = len(removed) // 2

    left = [node for node in range(len(graph)) if node not in removed]
    best_solution = calc_objective(graph, removed)
    best_removed = removed[:]
    current_solution = best_solution
    current_removed = removed[:]
    
    tabu_list = []

    i = 0

    # tabu loop
    while True:
        best_swap = None
        sol = -1
        for r in current_removed:
            for l in left:
                removed_copy = current_removed[:]
                removed_copy[removed_copy.index(r)] = l
                sol_swapped = calc_objective(graph, removed_copy)
                if (sol_swapped > sol and l not in tabu_list) or (sol_swapped > best_solution and l in tabu_list):
                    best_swap = (r, l)
                    sol = sol_swapped

        if best_swap[0] not in tabu_list:
            tabu_list.append(best_swap[0])
        
        if len(tabu_list) == n_tabu:
            del tabu_list[0]
        
        current_solution = sol
        current_removed[current_removed.index(best_swap[0])] = best_swap[1]
        left[left.index(best_swap[1])] = best_swap[0]
        #print([el for el in current_removed if el in left])

        i += 1

        if current_solution > best_solution:
            i = 0
            best_solution = current_solution
            best_removed = current_removed[:]
        
        if i == n_stall:
            break
    
    return best_removed


def best_1_swap(graph, removed):
    removed = removed[:]

    left = [node for node in range(len(graph)) if node not in removed]
    sol = calc_objective(graph, removed)
    best_swap = None
    for r in removed:
        for l in left:
            removed_copy = removed[:]
            removed_copy[removed_copy.index(r)] = l
            sol_swapped = calc_objective(graph, removed_copy)
            if sol_swapped > sol:
                best_swap = (r, l)
                sol = sol_swapped
    
    if best_swap is not None:
        r, l = best_swap
        removed[removed.index(r)] = l

    return removed


def first_improvement_2_swap(graph, removed):
    removed = removed[:]

    left = [node for node in range(len(graph)) if node not in removed]
    sol = calc_objective(graph, removed)
    best_swap = None
    for r1 in removed:
        for r2 in [r for r in removed if r != r1]:
            for l1 in left:
                for l2 in [l for l in left if l != l1]:
                    removed_copy = removed[:]
                    removed_copy[removed_copy.index(r1)] = l1
                    removed_copy[removed_copy.index(r2)] = l2
                    sol_swapped = calc_objective(graph, removed_copy)
                    if sol_swapped > sol:
                        removed[removed.index(r1)] = l1
                        removed[removed.index(r2)] = l2
                        return removed
    return removed

