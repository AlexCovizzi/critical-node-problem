import time
from greedy import algo_greedy, max_degree_best
from neighbor_search import best_1_swap, k_swap, tabu_search, first_improvement_2_swap
from graph import create_graph, calc_objective, create_graph_with_n_edges
from asp import global_optimum


def calc_errors(opt, sol):
    rel_error = ((opt - sol) / opt) * 100
    abs_error = opt - sol
    return rel_error, abs_error

def print_results(n_iter, abs_err, rel_err, time, improvement=None):
    print("Errore Assoluto medio: %.4f" % (abs_err/n_iter))
    print("Errore Relativo medio: %.4f %%" % (rel_err/n_iter))
    if improvement is not None:
        print("Miglioramento Relativo medio: %.4f %%" % (improvement/n_iter * 100))
    print("Tempo di calcolo medio: %.4f" % (time/n_iter))


if __name__ == "__main__":
    # Parametri del problema
    dim = 30
    k = 6
    threshold = None
    cconected = False
    n_edges = 75

    eval_iter = 10

    # Performance della Best 1-Swap
    best_1_swap_time = 0
    best_1_swap_abs_err = 0
    best_1_swap_rel_err = 0
    best_1_swap_rel_improvement = 0

    # Parametri del Random K-Swap
    k_s = k // 2 if k // 2 > 0 else 1
    n_iter = 100
    # Performance della Random K-Swap
    k_swap_time = 0
    k_swap_abs_err = 0
    k_swap_rel_err = 0
    k_swap_rel_improvement = 0
    
    # Performance della First-Improvement 2-Swap
    two_swap_time = 0
    two_swap_abs_err = 0
    two_swap_rel_err = 0
    two_swap_rel_improvement = 0

    # Parametri della Tabu Search
    n_tabu = k // 2 if k // 2 > 0 else 1
    n_stall = 100
    # Performance della Tabu Search
    tabu_time = 0
    tabu_abs_err = 0
    tabu_rel_err = 0
    tabu_rel_improvement = 0

    # Parametri della Variable Neighborhood Search
    moves = [best_1_swap, first_improvement_2_swap]
    # Performance della Variable Neighborhood Search
    vns_time = 0
    vns_abs_err = 0
    vns_rel_err = 0
    vns_rel_improvement = 0

    # Parametri della Multistart Search
    mss_n_start = 10
    mss_greedy_best = max_degree_best
    mss_stoc_dim = 5
    mss_move = best_1_swap
    # Performance della Variable Neighborhood Search
    mss_time = 0
    mss_abs_err = 0
    mss_rel_err = 0


    for i in range(eval_iter):
        print("Iterazione {}".format(i + 1))
        # Creazione del grafo e calcolo dell'ottimo globale
        if threshold:
            graph = create_graph(dim, threshold=threshold, connected=cconnected)
        else:
            graph = create_graph_with_n_edges(dim, edges=n_edges)
        n_connected = calc_objective(graph, [])

        opt, _ = global_optimum(graph, k)

        # genero la soluzione di partenza (Max Degree)
        start_removed = algo_greedy(graph, k, max_degree_best)
        start_sol = calc_objective(graph, start_removed)


        # Valutazione della Best 1-Swap
        one_swap_removed = start_removed
        one_swap_sol = start_sol

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
        
        rel_error, abs_error = calc_errors(opt, one_swap_sol)
        best_1_swap_abs_err += abs_error
        best_1_swap_rel_err += rel_error

        rel_imporovement = (one_swap_sol - start_sol) / one_swap_sol
        best_1_swap_rel_improvement += rel_imporovement

        best_1_swap_time += calc_time


        # Valutazione della k-Swap
        k_swap_sol = start_sol
        k_swap_removed = start_removed

        start_time = time.time()
        for i in range(n_iter):
            tmp_removed = k_swap(graph, k_swap_removed, k_s)
            tmp_sol = calc_objective(graph, tmp_removed)
            if tmp_sol >= k_swap_sol:
                k_swap_sol = tmp_sol
                k_swap_removed = tmp_removed

        calc_time = time.time() - start_time
        
        rel_error, abs_error = calc_errors(opt, k_swap_sol)
        k_swap_abs_err += abs_error
        k_swap_rel_err += rel_error

        rel_imporovement = (k_swap_sol - start_sol) / k_swap_sol
        k_swap_rel_improvement += rel_imporovement

        k_swap_time += calc_time


        # Valutazione della First Improvement 2-Swap
        two_swap_sol = start_sol
        two_swap_removed = start_removed

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
        
        rel_error, abs_error = calc_errors(opt, two_swap_sol)
        two_swap_abs_err += abs_error
        two_swap_rel_err += rel_error

        rel_imporovement = (two_swap_sol - start_sol) / two_swap_sol
        two_swap_rel_improvement += rel_imporovement

        two_swap_time += calc_time


        # Tabu Search
        
        tabu_removed = start_removed
        
        start_time = time.time()
        tabu_removed = tabu_search(graph, tabu_removed, n_tabu=n_tabu, n_stall=n_stall)
        tabu_sol = calc_objective(graph, tabu_removed)

        calc_time = time.time() - start_time
        
        rel_error, abs_error = calc_errors(opt,tabu_sol)
        tabu_abs_err += abs_error
        tabu_rel_err += rel_error

        rel_imporovement = (tabu_sol - start_sol) / tabu_sol
        tabu_rel_improvement += rel_imporovement

        tabu_time += calc_time


        # Valutazione Variable Neighborhood Search
        vns_removed = start_removed
        vns_sol = start_sol
        
        start_time = time.time()
        cont = 0
        tmp_removed = vns_removed
        while cont < len(moves):
            tmp_removed = moves[cont](graph, tmp_removed)
            tmp_sol = calc_objective(graph, tmp_removed)
            if tmp_sol > vns_sol:
                vns_removed = tmp_removed
                vns_sol = tmp_sol
                cont = 0
            else:
                cont += 1
        
        calc_time = time.time() - start_time
        
        rel_error, abs_error = calc_errors(opt, vns_sol)
        vns_abs_err += abs_error
        vns_rel_err += rel_error

        rel_imporovement = (vns_sol - start_sol) / vns_sol
        vns_rel_improvement += rel_imporovement

        vns_time += calc_time
        

        # Valutazione Multistart Search
        mss_best_removed = []
        mss_best_sol = 0

        start_time = time.time()
        for i in range(mss_n_start):
            mss_removed = algo_greedy(graph, k, mss_greedy_best, mss_stoc_dim)
            mss_sol = calc_objective(graph, mss_removed)

            tmp_removed = mss_removed
            while True:
                tmp_removed = mss_move(graph, tmp_removed)
                tmp_sol = calc_objective(graph, tmp_removed)

                if tmp_sol > mss_sol:
                    mss_sol = tmp_sol
                    mss_removed = tmp_removed
                else:
                    break
            
            if mss_sol > mss_best_sol:
                mss_best_sol = mss_sol
                mss_best_removed = mss_removed
        
        calc_time = time.time() - start_time

        rel_error, abs_error = calc_errors(opt, mss_sol)
        mss_abs_err += abs_error
        mss_rel_err += rel_error

        mss_time += calc_time

    print("\n-------------------------------------\n")

    # Stampa dei risultati
    print("Best 1-Swap")
    print_results(eval_iter, best_1_swap_abs_err, best_1_swap_rel_err, best_1_swap_time, best_1_swap_rel_improvement)

    print("\n-------------------------------------\n")

    print("Random K-Swap")
    print_results(eval_iter, k_swap_abs_err, k_swap_rel_err, k_swap_time, k_swap_rel_improvement)
    
    print("\n-------------------------------------\n")

    print("First-Improvement 2-Swap")
    print_results(eval_iter, two_swap_abs_err, two_swap_rel_err, two_swap_time, two_swap_rel_improvement)

    print("\n-------------------------------------\n")

    print("Tabu Search")
    print_results(eval_iter, tabu_abs_err, tabu_rel_err, tabu_time, tabu_rel_improvement)

    print("\n-------------------------------------\n")

    print("Variable Neighborhood Search")
    print_results(eval_iter, vns_abs_err, vns_rel_err, vns_time, vns_rel_improvement)

    print("\n-------------------------------------\n")

    print("Multistart Search")
    print_results(eval_iter, mss_abs_err, mss_rel_err, mss_time)