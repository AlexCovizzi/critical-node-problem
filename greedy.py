import random


def algo_greedy(graph, k, best, stoc_dim=1):
    removed = []
    for i in range(k):
        best_vertex = best(graph, removed, stoc_dim)
        removed.append(best_vertex)
    return removed



def create_population(graph, removed_nodes, pop_dim, bests, stoc_dim):
    population = []
    for i in range(pop_dim):
        random.shuffle(bests)
        individual = algo_greedy(graph, removed_nodes, bests[0], stoc_dim)
        population.append(individual)

    return population


def max_degree_best(graph, removed, k=1):
    deg_vertices = [sum([n for idx,n in enumerate(row) if idx not in removed]) for row in graph]
    best_vertices = []

    for i in removed:
        deg_vertices[i] = -1
    
    for i in range(k):
        max_deg = max(deg_vertices)
        max_vertex = deg_vertices.index(max_deg)
        best_vertices.append(max_vertex)
        deg_vertices[max_vertex] = -1
    
    random.shuffle(best_vertices)
    return best_vertices[0]


# buono con tanti nodi e grafo meno sparso
def min_conn_best(graph, removed, k=1):
    cur_best_couple = ()
    cur_best_val = 10000000
    deg_vertices = [sum([n for idx,n in enumerate(row) if idx not in removed]) for row in graph]

    best_couples = []

    for i in range(k):
        for node in range(len(graph)):
            if node in removed or deg_vertices[node] == 0:
                continue
            for node_2, conn in enumerate(graph[node]):
                if conn == 1 and node_2 not in removed and node_2 > node:
                    couple_degree = deg_vertices[node] + deg_vertices[node_2]
                    if couple_degree < cur_best_val and (node, node_2) not in best_couples:
                        cur_best_couple = (node, node_2)
                        cur_best_val = couple_degree
        
        best_couples.append(cur_best_couple)
    
    # restituisco il nodo con grado maggiore nella coppia
    random.shuffle(best_couples)
    cur_best_couple = best_couples[0]
    if deg_vertices[cur_best_couple[0]] > deg_vertices[cur_best_couple[1]]:
        return cur_best_couple[0]
    else:
        return cur_best_couple[1]


def min_conn_ratio_best(graph, removed, k=1):
    cur_best_couple = ()
    cur_best_val = -1
    deg_vertices = [sum([n for idx,n in enumerate(row) if idx not in removed]) for row in graph]

    best_couples = []
    
    for i in range(k):
        for node in range(len(graph)):
            if node in removed or deg_vertices[node] == 0:
                continue
            for node_2, conn in enumerate(graph[node]):
                if conn == 1 and node_2 not in removed and node_2 > node:
                    if deg_vertices[node] > deg_vertices[node_2]:
                        couple_degree = deg_vertices[node]/deg_vertices[node_2]
                    else:
                        couple_degree = deg_vertices[node_2]/deg_vertices[node]
                    if couple_degree > cur_best_val and (node, node_2) not in best_couples:
                        cur_best_couple = (node, node_2)
                        cur_best_val = couple_degree
            
        best_couples.append(cur_best_couple)
    
    # restituisco il nodo con grado maggiore nella coppia
    random.shuffle(best_couples)
    cur_best_couple = best_couples[0]
    if deg_vertices[cur_best_couple[0]] > deg_vertices[cur_best_couple[1]]:
        return cur_best_couple[0]
    else:
        return cur_best_couple[1]
