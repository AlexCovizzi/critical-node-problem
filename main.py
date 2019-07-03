import random
import time
import netgraph


def create_graph(n, threshold = 50):
    while True:
        graph = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            # Ogni riga avra' il proprio seme di casualita', dato dal tempo di sistema
            random.seed(int(time.clock() * 1000000))

            for j in range(i + 1, n):
                val = random.randint(0, 100)
                graph[i][j] = 0 if val <= threshold else 1
                graph[j][i] = graph[i][j]
        if is_connected(graph):
            return graph


def print_graph(graph, removed=[], f="graph.txt"):
    with open(f, "w") as f:
        for i in range(len(graph)):
            if i in removed:
                continue
            f.write(str(i) + "\n")
        
        for i in range(len(graph)):
            if i in removed:
                continue
            for j in range(i + 1, len(graph)):
                if j in removed:
                    continue
                if graph[i][j] == 1:
                    f.write(str(i) + " " + str(j) + "\n")


def algo_greedy(graph, k, best):
    removed = []
    for i in range(k):
        best_vertex = best(graph, removed)
        removed.append(best_vertex)
    return removed


def max_degree_best(graph, removed):
    deg_vertices = [sum([n for idx,n in enumerate(row) if idx not in removed]) for row in graph]
    for i in removed:
        deg_vertices[i] = -1
    max_deg = max(deg_vertices)
    max_vertex = deg_vertices.index(max_deg)
    return max_vertex

# buono con tanti nodi e grafo meno sparso
def min_conn_best(graph, removed):
    cur_best_couple = ()
    cur_best_val = 10000000
    deg_vertices = [sum([n for idx,n in enumerate(row) if idx not in removed]) for row in graph]
    for node in range(len(graph)):
        if node in removed or deg_vertices[node] == 0:
            continue
        for node_2, conn in enumerate(graph[node]):
            if conn == 1 and node_2 not in removed and node_2 > node:
                couple_degree = deg_vertices[node] + deg_vertices[node_2]
                if couple_degree < cur_best_val:
                    cur_best_couple = (node, node_2)
                    cur_best_val = couple_degree
    
    # restituisco il nodo con grado maggiore nella coppia
    if deg_vertices[cur_best_couple[0]] > deg_vertices[cur_best_couple[1]]:
        return cur_best_couple[0]
    else:
        return cur_best_couple[1]


def visit_connected(graph, i, visited):
    visited[i] = 1
    row = graph[i]
    for j in range(len(row)):
        if row[j] == 1 and visited[j] == 0:
            visit_connected(graph, j, visited)


def is_connected(graph):
    visited = [0 for row in graph]
    visit_connected(graph, 0, visited)

    if sum(visited) == len(visited):
        return True
    else:
        return False


def calc_objective(graph, removed):
    sol = 0
    visited = [0 for row in graph]

    # segna i nodi rimossi come visitati, cosi non vengono contati
    for i in removed:
        visited[i] = 1

    while sum(visited) != len(visited):
        index = visited.index(0)
        visit_connected(graph, index, visited)
        sol += 1
    
    return sol

def neighbour_search(graph, removed, mossa):
    best = calc_objective(graph, removed)

    while True:
        mossa(graph, removed)
        sol = calc_objective(graph, removed)
        if sol > best:
            best = sol
        else:
            shaking

def k_swap(graph, removed, k=1):
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


def tabu_search(graph, removed, n_tabu=None, n_stall=100):
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

        i += 1

        if current_solution > best_solution:
            i = 0
            best_solution = current_solution
            best_removed = current_removed[:]
        
        if i == n_stall:
            break
    
    removed.clear()
    removed.extend(best_removed)


def best_1_swap(graph, removed):
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


def first_improvement_2_swap(graph, removed):
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
                        return True


if __name__ == '__main__':
    graph = create_graph(40, threshold=85)

    k = 7
    
    removed = algo_greedy(graph, k, max_degree_best)

    best = calc_objective(graph, removed)

    print("max_degree")
    print(best)
    print(removed)

    removed_tabu_100 = removed[:]
    removed_tabu_1000 = removed[:]
    
    while True:
        best_1_swap(graph, removed)
        sol = calc_objective(graph, removed)
        if sol > best:
            best = sol
        else:
            break

    
    tabu_search(graph, removed_tabu_100, n_stall=100)
    best_tabu_100 = calc_objective(graph, removed_tabu_100)

    tabu_search(graph, removed_tabu_1000, n_stall=1000)
    best_tabu_1000 = calc_objective(graph, removed_tabu_1000)
    
    print("------------------------------")

    print("max_degree - 1-swap")
    print(best)
    print(removed)

    print("max_degree - tabu - 100")
    print(best_tabu_100)
    print(removed_tabu_100)

    print("max_degree - tabu - 1000")
    print(best_tabu_1000)
    print(removed_tabu_1000)
    