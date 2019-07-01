import random
import time


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


def print_graph(graph, f="graph.txt", removed=[]):
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


def algo_greedy(graph, k):
    graph1 = [row[:] for row in graph]
    removed = []
    for i in range(k):
        removed.append(algo_greedy_iter(graph1, removed))
    return graph1, removed


def algo_greedy_iter(graph, removed):
    best_vertex = first_best(graph, removed)
    # remove_vertex(graph, best_vertex)
    return best_vertex


def first_best(graph, removed):
    deg_vertices = [sum([n for idx,n in enumerate(row) if idx not in removed]) for row in graph]
    for i in removed:
        deg_vertices[i] = -1
    max_deg = max(deg_vertices)
    max_vertex = deg_vertices.index(max_deg)
    return max_vertex


def remove_vertex(graph, vertex):
    graph[vertex] = [0 for i in graph]
    for row in graph:
        row[vertex] = 0


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

if __name__ == '__main__':
    graph = create_graph(30, threshold=90)
    print_graph(graph, "graph_1.txt")
    graph_2, removed = algo_greedy(graph, 7)
    print_graph(graph_2, "graph_2.txt", removed)

    best = calc_objective(graph, removed)
    print(best)
    print(removed)
    while True:
        best_1_swap(graph, removed)
        sol = calc_objective(graph, removed)
        if sol > best:
            best = sol
        else:
            break
    
    print(removed)
    print(best)