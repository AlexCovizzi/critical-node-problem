from graph import create_graph
from graphdraw import GraphDraw
import time


def find_paths(graph, i, j, visited, mat):
    visited = visited[:]
    paths = []
    visited[i] = 1
    row = graph[i]

    if row[j] == 1:
        paths.append([i, j])
        return paths

    if mat[i][j]:
        return mat[i][j]

    for k in range(len(row)):
        if row[k] == 1 and visited[k] == 0:
            paths_kj = find_paths(graph, k, j, visited, mat)
            if k < j:
                mat[k][j] = paths_kj
            for path in paths_kj:
                paths.append([i] + path)
    
    return paths


def find_all_paths(graph):
    paths_mat = [ [ [] for i in graph] for j in graph]
    visited = [0 for i in range(len(graph))]
    for i in range(len(graph)):
        for j in range(i + 1, len(graph)):
            if not paths_mat[i][j]:
                paths = find_paths(graph, i, j, visited, paths_mat)
                paths_mat[i][j] = paths
    return paths_mat


if __name__ == "__main__":
    dim = 35
    thresh = 95
    connected = False
    graph = create_graph(dim, thresh, connected)
    draw = GraphDraw(graph)

    start_time = time.time()
    mat = find_all_paths(graph)
    print(str(time.time() - start_time))
    #for i in mat:
        #print(i)

    #draw.show()