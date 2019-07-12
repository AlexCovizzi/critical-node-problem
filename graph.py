import random
import time


def create_graph(n, threshold = 50, connected=True):
    while True:
        graph = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            # Ogni riga avra' il proprio seme di casualita', dato dal tempo di sistema
            random.seed(int(time.clock() * 1000000))

            for j in range(i + 1, n):
                val = random.randint(0, 100)
                graph[i][j] = 0 if val <= threshold else 1
                graph[j][i] = graph[i][j]
        if not connected or is_connected(graph):
            return graph


def create_graph_with_n_edges(n, edges=None):
    if edges is None:
        edges = 3 * n
    if edges > (n*n - n)//2:
        edges = (n*n - n)//2

    graph = [[0 for i in range(n)] for j in range(n)]
    for e in range(edges):
        i = random.randint(0, n - 2)
        j = random.randint(i + 1, n - 1)

        while graph[i][j] == 1:
            i = random.randint(0, n - 2)
            j = random.randint(i + 1, n - 1)
            
        graph[i][j] = 1
        graph[j][i] = graph[i][j]

    return graph

def visit_connected(graph, i, visited, removed=None):
    if removed is None or i not in removed:
        visited[i] = 1
        row = graph[i]
        for j in range(len(row)):
            if row[j] == 1 and visited[j] == 0:
                visit_connected(graph, j, visited, removed)


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


def couple_connected(graph, removed, i, j):
    visited = [0 for i in range(len(graph))]



def calc_alt_objective(graph, removed):
    sol = 0

    for i in range(len(graph)):
        visited = [0 for cont in range(len(graph))]
        if i not in removed:
            visit_connected(graph, i, visited, removed)
        else:
            visited[i] = 1
        sol += sum(visited)
    
    return sol
