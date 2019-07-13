import time
from greedy import algo_greedy, max_degree_best, min_conn_best, min_conn_ratio_best, create_population
from graph import create_graph, calc_objective, create_graph_with_n_edges
from genetic_algo import genetic_algo_binary, genetic_algo_removed, calc_dist
from asp import global_optimum


def calc_errors(opt, sol):
    rel_error = ((opt - sol) / opt) * 100
    abs_error = opt - sol
    return rel_error, abs_error


def print_results(n_iter, abs_err, rel_err, time):
    print("Errore Assoluto medio: %.4f" % (abs_err/n_iter))
    print("Errore Relativo medio: %.4f %%" % (rel_err/n_iter))
    print("Tempo di calcolo medio: %.4f" % (time/n_iter))


if __name__ == "__main__":
    dim = 30
    k = 8
    threshold = None
    cconnected = False
    n_edges = 90
    
    n_iter = 500
    
    # Parametri degli Algoritmi Genetici
    pop_dim = 30
    stoc_dim = 6
    n_parents = 8
    max_generations = 500
    bests = [max_degree_best, min_conn_best]

    pop_dist = 0

    ga_bin_abs_err = 0
    ga_bin_rel_err = 0
    ga_bin_time = 0

    ga_rem_abs_err = 0
    ga_rem_rel_err = 0
    ga_rem_time = 0

    for i in range(n_iter):
        print("Iterazione {}".format(i + 1))
        if threshold:
            graph = create_graph(dim, threshold=threshold, connected=cconnected)
        else:
            graph = create_graph_with_n_edges(dim, edges=n_edges)
        n_connected = calc_objective(graph, [])

        opt, _ = global_optimum(graph, k)
        
        population = create_population(graph, k, pop_dim, bests, stoc_dim)
        pop_dist += calc_dist(population)

        # Valutazione della Genetic Algo (Rappresentazione k interi)
        start_time = time.time()
        ga_rem_removed = genetic_algo_removed(graph, population, n_parents=n_parents, max_generations=max_generations)
        ga_rem_sol = calc_objective(graph, ga_rem_removed)
        calc_time = time.time() - start_time
        
        rel_error, abs_error = calc_errors(opt, ga_rem_sol)
        ga_rem_abs_err += abs_error
        ga_rem_rel_err += rel_error
        ga_rem_time += calc_time

        # Valutazione del Genetic Algo (rappresentazione binaria)
        start_time = time.time()
        ga_rem_removed = genetic_algo_binary(graph, population, n_parents=n_parents, max_generations=max_generations)
        ga_rem_sol = calc_objective(graph, ga_rem_removed)
        calc_time = time.time() - start_time
        
        rel_error, abs_error = calc_errors(opt, ga_rem_sol)
        ga_bin_abs_err += abs_error
        ga_bin_rel_err += rel_error
        ga_bin_time += calc_time
        
    print("\n-------------------------------------\n")

    print("Distanza media della popolazione: %.4f" % (pop_dist))
    
    print("\n-------------------------------------\n")

    # Stampa dei risultati
    print("Algoritmo Genetico - Codifica: Vettore a k interi")
    print_results(n_iter, ga_rem_abs_err, ga_rem_rel_err, ga_rem_time)

    print("\n-------------------------------------\n")

    print("Algoritmo Genetico - Codifica: Vettore binario")
    print_results(n_iter, ga_bin_abs_err, ga_bin_rel_err, ga_bin_time)