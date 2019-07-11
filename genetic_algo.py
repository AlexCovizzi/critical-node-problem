import random
from graph import calc_objective


# Come codifica, usiamo un vettore di k interi, con k numero di nodi rimossi
def genetic_algo_removed(graph, pop, n_parents=2, max_generations=100):
    # deep copy popolazione
    population = [e[:] for e in pop]
    k = len(population[0])
    max_pop = len(population)
    fitness_population = [calc_objective(graph, i) for i in population]

    if n_parents % 2 == 1:
        n_parents += 1

    n_gen = 0 # numero generazione
    while n_gen < max_generations:
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
                    while left[new_gene] in child_1:
                        new_gene = random.randint(0, len(left) - 1)
                    child_1[idx] = left[new_gene]
            for idx, gene in enumerate(child_2):
                if child_2.count(gene) > 1:
                    new_gene = random.randint(0, len(left) - 1)
                    while left[new_gene] in child_2:
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

    # Restituisco il migliore individuo
    max_fitness = max(fitness_population)
    idx = fitness_population.index(max_fitness)
    return population[idx]


# Come codifica, usiamo un vettore binario lungo n numero di nodi
def genetic_algo_binary(graph, pop, n_parents=2, max_generations=100):
    def to_binary(graph, removed):
        return [1 if i in removed else 0 for i in range(len(graph))]
    
    def to_removed(binary):
        return [i for i in range(len(binary)) if binary[i] == 1]

    # deep copy popolazione
    population = [e[:] for e in pop]

    k = len(population[0])
    max_pop = len(population)
    fitness_population = [calc_objective(graph, i) for i in population]

    if n_parents % 2 == 1:
        n_parents += 1

    n_gen = 0 # numero generazione
    while n_gen < max_generations:
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

        # Crossover dove eredito i geni in comune
        while index_parents:
            # Prendiamo i primi due genitori
            parent_1 = population[index_parents.pop()]
            parent_2 = population[index_parents.pop()]
            
            # Trasformiamo in binary
            parent_1 = to_binary(graph, parent_1)
            parent_2 = to_binary(graph, parent_2)

            child = [parent_1[i] if parent_1[i] == parent_2[i] else -1 for i in range(len(parent_1))]

            not_assigned = [i for i in range(len(child)) if child[i] == -1]
            genes_1 = random.sample(not_assigned, k - child.count(1))
            for gene in not_assigned:
                if gene in genes_1:
                    child[gene] = 1
                else:
                    child[gene] = 0

            # Passo di mutazione
            # Mutazione figlio
            mut_gene_1 = random.randint(0, len(child) - 1)
            mut_gene_2 = random.randint(0, len(child) - 1)
            while child[mut_gene_1] == child[mut_gene_2]:
                mut_gene_2 = random.randint(0, len(child) - 1)
            
            tmp = child[mut_gene_1]
            child[mut_gene_1] = child[mut_gene_2]
            child[mut_gene_2] = tmp

            # Il figlio è aggiunt alla popolazione
            child = to_removed(child)
            population.append(child)

        # Sostituzione generazionale
        fitness_population = [calc_objective(graph, i) for i in population]
        while len(population) > max_pop:
            min_fitness = min(fitness_population)
            idx = fitness_population.index(min_fitness)
            population.pop(idx)
            fitness_population.pop(idx)
        
        n_gen += 1

    # Restituisco il migliore individuo
    max_fitness = max(fitness_population)
    idx = fitness_population.index(max_fitness)
    return population[idx]