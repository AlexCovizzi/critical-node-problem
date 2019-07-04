import random
import time
import netgraph
import subprocess
import sys


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


def print_asp(graph, rem, out="problema.pl"):
    with open(out, "w") as f:
        for i in range(len(graph)):
            f.write("nodo(" + str(i) + ")." + "\n")
        
        for i in range(len(graph)):
            for j in range(i + 1, len(graph)):
                if graph[i][j] == 1:
                    f.write("arco(" + str(i) + ", " + str(j) + ")." + "\n")
        
        f.write("rem(" + str(k) + ").")

        with open("critical-node.pl", "r") as model:
            text = model.read()
            f.write(text)


def algo_greedy(graph, k, best, stoc_dim=1):
    removed = []
    for i in range(k):
        best_vertex = best(graph, removed, stoc_dim)
        removed.append(best_vertex)
    return removed


def max_degree_best(graph, removed, k=1):
    deg_vertices = [sum([n for idx,n in enumerate(row) if idx not in removed]) for row in graph]
    best_vertices = []

    for i in removed:
        deg_vertices[i] = -1
    
    for i in range(k):
        max_deg = max(deg_vertices)
        max_vertex = deg_vertices.index(max_deg)
        best_vertices.append(max_vertex)
        deg_vertices.pop(max_vertex)
    
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


# TODO: in una soluzione sono venuti dei valori ripetuti WTF!
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


def global_optimum(graph, k, asp_name="problema.pl"):
    print_asp(graph, k, asp_name)

    asp_output = subprocess.run(['clingo', asp_name], stdout=subprocess.PIPE).stdout.decode('utf-8')
    with open("asp-output", "w") as f:
        f.write(asp_output)
    
    with open("asp-output", "r") as f:
        if sys.platform.startswith('win'):
            result = f.readlines()[-20]
        else:
            result = f.readlines()[-10]
    
    atoms = result.split()
    asp_removed = []
    asp_sol = None
    for atom in atoms:
        if atom.startswith("removed"):
            atom = atom[:-1]
            node = int(atom[8:])
            asp_removed.append(node)
        if atom.startswith("conta"):
            atom = atom[:-1]
            asp_sol = int(atom[6:])
    
    return asp_sol, asp_removed


def create_population(graph, removed_nodes, pop_dim, bests, stoc_dim):
    population = []
    for i in range(pop_dim):
        random.shuffle(bests)
        individual = algo_greedy(graph, removed_nodes, bests[0], stoc_dim)
        population.append(individual)

    return population


# Come codifica, usiamo un vettore di k interi
def genetic_algo_removed(graph, population, n_parents=2, max_generations=100):
    k = len(population[0])
    max_pop = len(population)
    fitness_population = [calc_objective(graph, i) for i in population]

    if n_parents % 2 == 1:
        n_parents += 1

    n_gen = 0 # numero generazione
    while True:
        ''' [2, 4, 1, 3] -> [4, 6, 7, 10] '''
        selection_list = []
        for fitness_removed in fitness_population:
            if selection_list == []:
                selection_list.append(fitness_removed)
            else:
                selection_list.append(fitness_removed + selection_list[-1])
        
        # Selezione dell'indice dei genitori
        index_parents = []
        while len(index_parents) != n_parents:
            selected = random.randint(1, selection_list[-1])
            for idx in range(len(selection_list)):
                if selected <= selection_list[0]:
                    if 0 not in index_parents:
                        index_parents.append(0)
                    break
                if selected <= selection_list[idx] and selected > selection_list[idx-1]:
                    if idx not in index_parents:
                        index_parents.append(idx)
                    break

        # Crossover a maschera binaria
        while index_parents:
            ''' 010110 -> padre | 101001 -> madre | doppioni!! '''
            mask = [random.randint(0, 1) for i in range(k)]
            # Prendiamo i primi due genitori
            parent_1 = population[index_parents.pop()]
            parent_2 = population[index_parents.pop()]

            left = [i for i in range(len(graph)) if i not in parent_1 and i not in parent_2]

            child_1 = []
            child_2 = []

            for idx, bit in enumerate(mask):
                if bit == 0:
                    child_1.append(parent_1[idx])
                    child_2.append(parent_2[idx])
                elif bit == 1:
                    child_1.append(parent_2[idx])
                    child_2.append(parent_1[idx])

            # scambio i doppioni nei figli
            for idx, gene in enumerate(child_1):
                if child_1.count(gene) > 1:
                    new_gene = random.randint(0, len(left) - 1)
                    while new_gene in child_1:
                        new_gene = random.randint(0, len(left) - 1)
                    child_1[idx] = left[new_gene]
            for idx, gene in enumerate(child_2):
                if child_2.count(gene) > 1:
                    new_gene = random.randint(0, len(left) - 1)
                    while new_gene in child_2:
                        new_gene = random.randint(0, len(left) - 1)
                    child_2[idx] = left[new_gene]

            # Passo di mutazione
            # Mutazione figlio 1
            mut_gene = random.randint(0, len(child_1) - 1)
            offset = random.randint(1, 1000)
            new_value = (child_1[mut_gene] + offset) % len(graph)
            while new_value in child_1:
                offset = random.randint(1, 1000)
                new_value = (child_1[mut_gene] + offset) % len(graph)
            child_1[mut_gene] = new_value

            # Mutazione figlio 2
            mut_gene = random.randint(0, len(child_2) - 1)
            offset = random.randint(1, 1000)
            new_value = (child_2[mut_gene] + offset) % len(graph)
            while new_value in child_1:
                offset = random.randint(1, 1000)
                new_value = (child_2[mut_gene] + offset) % len(graph)
            child_2[mut_gene] = new_value

            # I due figli sono aggiunti alla popolazione
            population.append(child_1)
            population.append(child_2)

        # Sostituzione generazionale
        fitness_population = [calc_objective(graph, i) for i in population]
        while len(population) > max_pop:
            min_fitness = min(fitness_population)
            idx = fitness_population.index(min_fitness)
            population.pop(idx)
            fitness_population.pop(idx)
        
        n_gen += 1
        # Condizione di stop
        if n_gen == max_generations:
            break
    # Restituisco il migliore individuo
    max_fitness = max(fitness_population)
    idx = fitness_population.index(max_fitness)
    return population[idx]


if __name__ == '__main__':
    graph = create_graph(75, threshold=90)

    k = 20
    """
    opt, opt_removed = global_optimum(graph, k)
    
    print("Global optimum")
    print(opt)
    opt_removed.sort()
    print(opt_removed)
    """

    print("------------------------------")

    bests = [max_degree_best, min_conn_best, min_conn_ratio_best]

    population = create_population(graph, k, 20, bests, 5)
    removed_tabu = population[0][:]
    removed = genetic_algo_removed(graph, population, n_parents=4, max_generations=50)
    
    print("Genetic optimum")
    print(calc_objective(graph, removed))
    removed.sort()
    print(removed)

    """
    while True:
        best_1_swap(graph, removed)
        sol = calc_objective(graph, removed)
        if sol > best:
            best = sol
        else:
            break
    """
    
    tabu_search(graph, removed_tabu, n_tabu=k-3, n_stall=100)
    best_tabu = calc_objective(graph, removed_tabu)
    
    print("------------------------------")

    print("tabu - 100")
    print(best_tabu)
    removed_tabu.sort()
    print(removed_tabu)
    
