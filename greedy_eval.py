import time
from greedy import algo_greedy, max_degree_best, min_conn_best, min_conn_ratio_best, create_population
from graph import create_graph, calc_objective, create_graph_with_n_edges
from asp import global_optimum


def calc_errors(opt, sol):
    rel_error = ((opt - sol) / opt) * 100
    abs_error = opt - sol
    return rel_error, abs_error


if __name__ == "__main__":
    dim = 30
    k = 8
    threshold = None
    cconnected = False
    n_edges = 90
    
    n_iter = 500

    max_degree_time = 0
    min_conn_time = 0
    min_conn_ratio_time = 0

    max_degree_abs_err = 0
    min_conn_abs_err = 0
    min_conn_ratio_abs_err = 0

    max_degree_rel_err = 0
    min_conn_rel_err = 0
    min_conn_ratio_rel_err = 0

    for i in range(n_iter):
        print("Iterazione {}".format(i + 1))
        if threshold:
            graph = create_graph(dim, threshold=threshold, connected=cconnected)
        else:
            graph = create_graph_with_n_edges(dim, edges=n_edges)
        n_connected = calc_objective(graph, [])

        opt, _ = global_optimum(graph, k)

        # Valutazione della Max Degree Best
        start_time = time.time()
        max_degree_removed = algo_greedy(graph, k, max_degree_best)
        max_degree_sol = calc_objective(graph, max_degree_removed)
        calc_time = time.time() - start_time
        
        rel_error, abs_error = calc_errors(opt, max_degree_sol)
        max_degree_abs_err += abs_error
        max_degree_rel_err += rel_error
        max_degree_time += calc_time

        # Valutazione della Min Connection Best
        start_time = time.time()
        min_conn_removed = algo_greedy(graph, k, min_conn_best)
        min_conn_sol = calc_objective(graph, min_conn_removed)
        calc_time = time.time() - start_time

        rel_error, abs_error = calc_errors(opt, min_conn_sol)
        min_conn_abs_err += abs_error
        min_conn_rel_err += rel_error
        min_conn_time += calc_time

        # Valutazione della Min Connection Ratio Best
        start_time = time.time()
        min_conn_ratio_removed = algo_greedy(graph, k, min_conn_ratio_best)
        min_conn_ratio_sol = calc_objective(graph, min_conn_ratio_removed)
        calc_time = time.time() - start_time
        
        rel_error, abs_error = calc_errors(opt, min_conn_ratio_sol)
        min_conn_ratio_abs_err += abs_error
        min_conn_ratio_rel_err += rel_error
        min_conn_ratio_time += calc_time
    
    # Stampa dei risultati
    print("Max Degree")
    print("Errore Assoluto medio: %.4f" % (max_degree_abs_err/n_iter))
    print("Errore Relativo medio: %.4f %%" % (max_degree_rel_err/n_iter))
    print("Tempo di calcolo medio: %.4f" % (max_degree_time/n_iter))

    print("\n-------------------------------------\n")

    print("Min Connection")
    print("Errore Assoluto medio: %.4f" % (min_conn_abs_err/n_iter))
    print("Errore Relativo medio: %.4f %%" % (min_conn_rel_err/n_iter))
    print("Tempo di calcolo medio: %.4f" % (min_conn_time/n_iter))

    print("\n-------------------------------------\n")

    print("Min Connection Ratio")
    print("Errore Assoluto medio: %.4f" % (min_conn_ratio_abs_err/n_iter))
    print("Errore Relativo medio: %.4f %%" % (min_conn_ratio_rel_err/n_iter))
    print("Tempo di calcolo medio: %.4f" % (min_conn_ratio_time/n_iter))
    