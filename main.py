def create_graph(n):
    return []


def algo_greedy(graph, k):
    graph1 = [row[:] for row in graph]
    removed = []
    for i in range(k):
        removed.append(algo_greedy_iter(graph1))
    return graph1, removed


def algo_greedy_iter(graph):
    best_vertex = first_best(graph)
    remove_vertex(graph, best_vertex)
    return best_vertex


def first_best(graph):
    deg_vertices = [sum(row) for row in graph]
    max_deg = max(deg_vertices)
    max_vertex = deg_vertices.index(max_deg)
    return max_vertex


def remove_vertex(graph, vertex):
    graph[vertex] = [0 for i in graph]
    for row in graph:
        row[vertex] = 0

def calc_objective(graph, removed):
    def calc_rec(graph, i, visited):
        visited[i] = 1
        row = graph[i]
        for j in range(len(row)):
            if row[j] == 1 and visited[j] == 0:
                calc_rec(graph, j, visited)

    sol = 0
    visited = [0 for row in graph]
    for i in removed:
        visited[i] = 1

    while sum(visited) != len(visited):
        index = visited.index(0)
        calc_rec(graph, index, visited)
        sol += 1
    
    return sol


graph = create_graph(4)
graph = [
    [0, 1, 0, 1, 1, 0],
    [1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 0],
]
greedy_sol, removed = algo_greedy(graph, 2)

sol = calc_objective(greedy_sol, removed)

print(removed)
print(sol)