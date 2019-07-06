import time
from graphdraw import GraphDraw
from greedy import *
from graph import *
from asp import *
from neighbor_search import *
from genetic_algo import *


def calc_errors(opt, sol):
    rel_error = ((opt - sol) / opt) * 100
    abs_error = opt - sol
    return rel_error, abs_error

def print_solution(removed, sol, opt, calc_time):
    rel_error, abs_error = calc_errors(opt, sol)
    
    removed = removed[:]
    removed.sort()
    print("Tempo di calcolo (in sec): %.3f" % calc_time)
    print("Soluzione trovata: {}".format(sol))
    print("Nodi rimossi: {}".format(removed))
    print("Errore relativo: %.1f %%" % rel_error)
    print("Errore assoluto: {}".format(abs_error))


if __name__ == '__main__':
    # Creiamo un grafo di 30 nodi: toglieremo 7 nodi da esso
    dim = 35
    graph = create_graph(dim, threshold=90, connected=False)
    n_connected = calc_objective(graph, [])
    k = 7

    print("Dimensione del grafo: {}".format(dim))
    print("Numero di nodi da rimuovere: {}".format(k))
    print("Componenti connesse nel grafo di partenza: {}".format(n_connected))

    draw = GraphDraw(graph)

    draw.show()

    # Ottimo globale
    print("\n-------------------------------------\n")
    start_time = time.time()
    opt, opt_removed = global_optimum(graph, k)
    calc_time = time.time() - start_time

    opt_removed.sort()
    print("Ottimo globale: {}".format(opt))
    print("Nodi rimossi: {}".format(opt_removed))
    print("Tempo di calcolo (in sec): %.3f" % calc_time)

    draw.show(opt_removed)

    # Applichiamo le greeedy
    print("\n-------------------------------------\n")
    print("Max Degree Greedy")
    start_time = time.time()
    max_degree_removed = algo_greedy(graph, k, max_degree_best)
    max_degree_sol = calc_objective(graph, max_degree_removed)

    calc_time = time.time() - start_time
    
    print_solution(max_degree_removed, max_degree_sol, opt, calc_time)

    draw.show(max_degree_removed)
    
    print("\n")

    print("Min Connection Greedy")
    start_time = time.time()
    min_conn_removed = algo_greedy(graph, k, min_conn_best)
    min_conn_sol = calc_objective(graph, min_conn_removed)

    calc_time = time.time() - start_time

    print_solution(min_conn_removed, min_conn_sol, opt, calc_time)

    draw.show(min_conn_removed)

    print("\n")

    print("Min Connection Ratio Greedy")
    start_time = time.time()
    min_conn_ratio_removed = algo_greedy(graph, k, min_conn_ratio_best)
    min_conn_ratio_sol = calc_objective(graph, min_conn_ratio_removed)

    calc_time = time.time() - start_time
    
    print_solution(min_conn_ratio_removed, min_conn_ratio_sol, opt, calc_time)

    draw.show(min_conn_ratio_removed)

    # Applichiamo le euristiche
    print("\n-------------------------------------\n")
    print("K-Swap Casuale")
    print("Soluzione di partenza (Max Degree): {} ({})".format(max_degree_removed, max_degree_sol))

    k_swap_sol = max_degree_sol
    k_swap_removed = max_degree_removed

    k_s = k // 2
    n_iter = 100

    print("\nEseguiamo {} iterazioni, facendo uno swap casuale di {} elementi ad ogni iterazione\n".format(n_iter, k_s))

    start_time = time.time()
    for i in range(n_iter):
        tmp_removed = k_swap(graph, k_swap_removed, k_s)
        tmp_sol = calc_objective(graph, tmp_removed)
        if tmp_sol >= k_swap_sol:
            k_swap_sol = tmp_sol
            k_swap_removed = tmp_removed

    calc_time = time.time() - start_time
    
    print_solution(k_swap_removed, k_swap_sol, opt, calc_time)

    improvement = k_swap_sol - max_degree_sol
    print("Miglioramento: {}".format(improvement))
    
    draw.show(k_swap_removed)

    print("\n-------------------------------------\n")
    print("Best 1-Swap")
    print("Soluzione di partenza (Max Degree): {} ({})".format(max_degree_removed, max_degree_sol))

    one_swap_sol = max_degree_sol
    one_swap_removed = max_degree_removed

    print("\nEseguiamo la migliore mossa di 1-swap, fino al suo ottimo locale\n")

    start_time = time.time()
    while True:
        tmp_removed = best_1_swap(graph, one_swap_removed)
        tmp_sol = calc_objective(graph, tmp_removed)

        if tmp_sol > one_swap_sol:
            one_swap_sol = tmp_sol
            one_swap_removed = tmp_removed
        else:
            break

    calc_time = time.time() - start_time
    
    print_solution(one_swap_removed, one_swap_sol, opt, calc_time)

    improvement = one_swap_sol - max_degree_sol
    print("Miglioramento: {}".format(improvement))
    
    draw.show(one_swap_removed)

    print("\n-------------------------------------\n")
    print("First Improvement 2-Swap")
    print("Soluzione di partenza (Max Degree): {} ({})".format(max_degree_removed, max_degree_sol))

    two_swap_sol = max_degree_sol
    two_swap_removed = max_degree_removed

    print("\nEseguiamo una mossa di 2-swap fino al primo miglioramento: iteriamo fino al suo ottimo locale\n")

    start_time = time.time()
    while True:
        tmp_removed = first_improvement_2_swap(graph, two_swap_removed)
        tmp_sol = calc_objective(graph, tmp_removed)

        if tmp_sol > two_swap_sol:
            two_swap_sol = tmp_sol
            two_swap_removed = tmp_removed
        else:
            break

    calc_time = time.time() - start_time
    
    print_solution(two_swap_removed, two_swap_sol, opt, calc_time)

    improvement = two_swap_sol - max_degree_sol
    print("Miglioramento: {}".format(improvement))

    draw.show(two_swap_removed)

    print("\n-------------------------------------\n")
    print("Tabu Search con mossa di 1-swap")
    print("Soluzione di partenza (Max Degree): {} ({})".format(max_degree_removed, max_degree_sol))

    tabu_removed = max_degree_removed

    n_tabu = k // 2
    n_stall = 100

    print("\nEseguiamo una tabu search, con una lista tabu lunga al massimo {}, con condizione di stop il non avere miglioramenti per {} passi\n".format(n_tabu, n_stall))

    start_time = time.time()
    tabu_removed = tabu_search(graph, tabu_removed, n_tabu=n_tabu, n_stall=n_stall)
    tabu_sol = calc_objective(graph, tabu_removed)

    calc_time = time.time() - start_time
    
    print_solution(tabu_removed, tabu_sol, opt, calc_time)

    improvement = tabu_sol - max_degree_sol
    print("Miglioramento: {}".format(improvement))

    draw.show(tabu_removed)

    print("\n-------------------------------------\n")
    pop_dim = 30
    stoc_dim = 5
    print("Creiamo una popolazione di {} individui per gli algoritmi genetici".format(pop_dim))
    population = create_population(graph, k, pop_dim, [max_degree_best, min_conn_best, min_conn_ratio_best], stoc_dim)

    n_parents = 4
    max_generations = 500
    print("Generiamo un totale di {} generazioni e ad ogni generazione verranno scelti {} genitori\n".format(max_generations, n_parents))

    print("Algoritmo genetico, codifica: vettore a {} interi".format(k))

    start_time = time.time()
    genetic_removed = genetic_algo_removed(graph, population, n_parents, max_generations)
    genetic_sol = calc_objective(graph, genetic_removed)

    calc_time = time.time() - start_time
    
    print_solution(genetic_removed, genetic_sol, opt, calc_time)

    draw.show(genetic_removed)

    print("\nAlgoritmo genetico, codifica: vettore binario di {} elementi".format(dim))

    start_time = time.time()
    genetic_bin_removed = genetic_algo_binary(graph, population, n_parents, max_generations)
    genetic_bin_sol = calc_objective(graph, genetic_removed)

    calc_time = time.time() - start_time
    
    print_solution(genetic_bin_removed, genetic_bin_sol, opt, calc_time)

    draw.show(genetic_bin_removed)

    print("\n-------------------------------------\n")
    ris = ""
    while ris != "y" and ris != "n":
        ris = input("Salva grafo? [y/n]")
    if ris == "y":
        name = input("Mettice il nome, aooooo: ")
        with open(name, "w+") as f:
            f.write(str(graph))