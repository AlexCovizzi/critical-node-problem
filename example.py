import time
from graphdraw import GraphDraw
from greedy import algo_greedy, max_degree_best, min_conn_best, min_conn_ratio_best, create_population
from graph import create_graph, calc_objective, create_graph_with_n_edges, calc_alt_objective
from asp import global_optimum
from minizinc import relaxed_optimum
from neighbor_search import k_swap, best_1_swap, first_improvement_2_swap, tabu_search
from genetic_algo import genetic_algo_binary, genetic_algo_removed, calc_dist


def calc_errors(opt, sol):
    rel_error = ((opt - sol) / opt) * 100
    abs_error = opt - sol
    return rel_error, abs_error

def print_solution(removed, sol, alt_sol, opt, alt_opt, calc_time):
    if opt:
        rel_error, abs_error = calc_errors(opt, sol)
    elif alt_opt:
        rel_error, abs_error = calc_errors(alt_opt, alt_sol)

    removed = removed[:]
    removed.sort()
    print("Tempo di calcolo (in sec): %.3f" % calc_time)
    print("Soluzione trovata: {}".format(sol))
    print("Soluzione alternativa trovata: {}".format(alt_sol))
    print("Nodi rimossi: {}".format(removed))
    if opt or alt_opt:
        print("Errore relativo: %.1f %%" % rel_error)
        print("Errore assoluto: {}".format(abs_error))


def create_dat(graph, k, out="cndp.dat"):
    with open(out, "w+") as f:
        f.write("N_NODES : {}\n".format(len(graph)))
        f.write("K : {}\n".format(k))
        f.write("ARCHI :\n[{}]".format("\n".join([" ".join([str(c) for c in r]) for r in graph])))

def count_edges(graph):
    counter = 0
    for i in range(len(graph)):
        for j in range(i+1, len(graph)):
            counter += graph[i][j]
    return counter


if __name__ == '__main__':
    # Dati del problema
    dim = 30
    k = 10
    threshold = None
    cconnected = True
    n_edges = 100
    ddraw = False

    #Boolean di controllo
    gglobal_optimum = False
    rrelaxed_optimum = True
    max_degree = True
    min_connection = True
    min_connection_ratio = True
    random_k_swap = False
    bbest_1_swap = False
    fi_2_swap = False
    tabu = False
    variable_neighborhood_search = False
    multistart_search = False
    ggenetic_removed = False
    genetic_binary = False
    save = False

    # Parametri del Random K-Swap
    k_s = k // 2 if k // 2 > 0 else 1
    n_iter = 100

    # Parametri della Tabu Search
    n_tabu = k // 2 if k // 2 > 0 else 1
    n_stall = 100

    # Parametri della Variable Neighborhood Search
    moves = [best_1_swap, first_improvement_2_swap]

    # Parametri della Multistart Search
    mss_n_start = 10
    mss_greedy_best = max_degree_best
    mss_stoc_dim = 5
    mss_move = best_1_swap

    # Parametri degli Algoritmi Genetici
    pop_dim = 30
    stoc_dim = 5
    n_parents = 8
    max_generations = 500

    if threshold:
        graph = create_graph(dim, threshold=threshold, connected=cconnected)
    else:
        graph = create_graph_with_n_edges(dim, edges=n_edges)
    n_connected = calc_objective(graph, [])
    n_edges = count_edges(graph)

    print("Dimensione del grafo: {}".format(dim))
    print("Numero di archi: {}".format(n_edges))
    print("Numero di nodi da rimuovere: {}".format(k))
    print("Componenti connesse nel grafo di partenza: {}".format(n_connected))

    if ddraw:
        draw = GraphDraw(graph)

        draw.show()

    # Ottimo globale
    print("\n-------------------------------------\n")
    if gglobal_optimum:
        print("Ottimo globale")
        start_time = time.time()
        global_opt, opt_removed = global_optimum(graph, k)
        global_alt_sol = calc_alt_objective(graph, opt_removed)

        calc_time = time.time() - start_time

        opt_removed.sort()
        print("Ottimo globale: {}".format(global_opt))
        print("Nodi rimossi: {}".format(opt_removed))
        print("Tempo di calcolo (in sec): %.3f" % calc_time)
        
        print("Soluzione alternativa: {}".format(global_alt_sol))

        if ddraw:
            draw.show(opt_removed)
        
        print("\n-------------------------------------\n")
    
    # Ottimo rilassato
    if rrelaxed_optimum:
        print("Ottimo rilassato")
        start_time = time.time()
        sol_mzn, removed_mzn = relaxed_optimum(graph, k)
        calc_time = time.time() - start_time
        relaxed_opt = calc_objective(graph, removed_mzn)

        print("Soluzione rilassata: {}".format(sol_mzn))
        print("Ottimo rilassato: {}".format(relaxed_opt))
        print("Nodi rimossi: {}".format(removed_mzn))
        print("Tempo di calcolo (in sec): %.3f" % calc_time)
        
        print("\n-------------------------------------\n")

    if global_optimum:
        opt = global_opt
        alt_opt = global_alt_sol
    elif rrelaxed_optimum:
        opt = None
        alt_opt = relaxed_optimum
    else:
        opt = None
        alt_opt = None

    # Applichiamo le greeedy
    if max_degree or random_k_swap or bbest_1_swap or fi_2_swap or tabu:
        print("Max Degree Greedy")
        start_time = time.time()
        max_degree_removed = algo_greedy(graph, k, max_degree_best)
        max_degree_sol = calc_objective(graph, max_degree_removed)
        max_degree_alt_sol = calc_alt_objective(graph, max_degree_removed)

        calc_time = time.time() - start_time

        print_solution(max_degree_removed, max_degree_sol, max_degree_alt_sol, opt, alt_opt, calc_time)

        if ddraw:
            draw.show(max_degree_removed)
    
        print("\n-------------------------------------\n")

    if min_connection:
        print("Min Connection Greedy")
        start_time = time.time()
        min_conn_removed = algo_greedy(graph, k, min_conn_best)
        min_conn_sol = calc_objective(graph, min_conn_removed)
        min_conn_alt_sol = calc_alt_objective(graph, min_conn_removed)

        calc_time = time.time() - start_time

        print_solution(min_conn_removed, min_conn_sol, min_conn_alt_sol, opt, alt_opt, calc_time)

        if ddraw:
            draw.show(min_conn_removed)

        print("\n-------------------------------------\n")

    if min_connection_ratio:
        print("Min Connection Ratio Greedy")
        start_time = time.time()
        min_conn_ratio_removed = algo_greedy(graph, k, min_conn_ratio_best)
        min_conn_ratio_sol = calc_objective(graph, min_conn_ratio_removed)
        min_conn_ratio_alt_sol = calc_alt_objective(graph, min_conn_ratio_removed)

        calc_time = time.time() - start_time

        
        print_solution(min_conn_ratio_removed, min_conn_ratio_sol, min_conn_ratio_alt_sol, opt, alt_opt, calc_time)

        if ddraw:
            draw.show(min_conn_ratio_removed)

        print("\n-------------------------------------\n")
    
    # Applichiamo le euristiche
    if random_k_swap:
        print("K-Swap Casuale")
        print("Soluzione di partenza (Max Degree): {} ({})".format(max_degree_removed, max_degree_sol))

        k_swap_sol = max_degree_sol
        k_swap_removed = max_degree_removed

        print("\nEseguiamo {} iterazioni, facendo uno swap casuale di {} elementi ad ogni iterazione\n".format(n_iter, k_s))

        start_time = time.time()
        for i in range(n_iter):
            tmp_removed = k_swap(graph, k_swap_removed, k_s)
            tmp_sol = calc_objective(graph, tmp_removed)
            if tmp_sol >= k_swap_sol:
                k_swap_sol = tmp_sol
                k_swap_removed = tmp_removed

        k_swap_alt_sol = calc_alt_objective(graph, k_swap_removed)
        calc_time = time.time() - start_time

        
        print_solution(k_swap_removed, k_swap_sol, k_swap_alt_sol, opt, alt_opt, calc_time)

        improvement = k_swap_sol - max_degree_sol
        print("Miglioramento: {}".format(improvement))
        
        if ddraw:
            draw.show(k_swap_removed)

        print("\n-------------------------------------\n")
    
    if bbest_1_swap:
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

        one_swap_alt_sol = calc_alt_objective(graph, one_swap_removed)
        calc_time = time.time() - start_time

        print_solution(one_swap_removed, one_swap_sol, one_swap_alt_sol, opt, alt_opt, calc_time)

        improvement = one_swap_sol - max_degree_sol
        print("Miglioramento: {}".format(improvement))
        
        if ddraw:
            draw.show(one_swap_removed)

        print("\n-------------------------------------\n")

    if fi_2_swap:
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

        two_swap_alt_sol = calc_alt_objective(graph, two_swap_removed)
        calc_time = time.time() - start_time

        print_solution(two_swap_removed, two_swap_sol, two_swap_alt_sol, opt, alt_opt, calc_time)

        improvement = two_swap_sol - max_degree_sol
        print("Miglioramento: {}".format(improvement))

        if ddraw:
            draw.show(two_swap_removed)

        print("\n-------------------------------------\n")
    
    if tabu:
        print("Tabu Search con mossa di 1-swap")
        print("Soluzione di partenza (Max Degree): {} ({})".format(max_degree_removed, max_degree_sol))

        tabu_removed = max_degree_removed

        print("\nEseguiamo una tabu search, con una lista tabu lunga al massimo {}, con condizione di stop il non avere miglioramenti per {} passi\n".format(n_tabu, n_stall))

        start_time = time.time()
        tabu_removed = tabu_search(graph, tabu_removed, n_tabu=n_tabu, n_stall=n_stall)
        tabu_sol = calc_objective(graph, tabu_removed)
        tabu_alt_sol = calc_alt_objective(graph, tabu_removed)

        calc_time = time.time() - start_time
        
        print_solution(tabu_removed, tabu_sol, tabu_alt_sol, opt, alt_opt, calc_time)

        improvement = tabu_sol - max_degree_sol
        print("Miglioramento: {}".format(improvement))

        if ddraw:
            draw.show(tabu_removed)

        print("\n-------------------------------------\n")

    if variable_neighborhood_search:
        print("Variable Neighborhood Search con Best-1-Swap e First Improvement 2-Swap")

        print("Soluzione di partenza (Max Degree): {} ({})".format(max_degree_removed, max_degree_sol))

        vns_removed = max_degree_removed
        vns_sol = max_degree_sol

        print("\nEseguiamo una VNS, con le mosse fornite: seguiremo un approccio di tipo descent\n")
        
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
        
        vns_alt_sol = calc_alt_objective(graph, vns_removed)
        calc_time = time.time() - start_time
        
        print_solution(vns_removed, vns_sol, vns_alt_sol, opt, alt_opt, calc_time)

        improvement = vns_sol - max_degree_sol
        print("Miglioramento: {}".format(improvement))

        if ddraw:
            draw.show(vns_removed)

        print("\n-------------------------------------\n")

    if multistart_search:
        print("Multistart Search")

        print("\nEseguiamo una Multistart Search, con la mossa fornita, per un totale di {} diverse ricerche\n".format(mss_n_start))
        
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
        
        mss_alt_sol = calc_alt_objective(graph, mss_removed)
        calc_time = time.time() - start_time
        
        print_solution(mss_removed, mss_sol, mss_alt_sol, opt, alt_opt, calc_time)

        if ddraw:
            draw.show(mss_removed)
        
        print("\n-------------------------------------\n")

    if genetic_algo_binary or genetic_algo_removed:
        print("Creiamo una popolazione di {} individui per gli algoritmi genetici".format(pop_dim))
        population = create_population(graph, k, pop_dim, [max_degree_best, min_conn_best, min_conn_ratio_best], stoc_dim)
        pop_dist = calc_dist(population)
        print("La popolazione ha una distanza media di %.4f" % pop_dist)

        print("Generiamo un totale di {} generazioni e ad ogni generazione verranno scelti {} genitori\n".format(max_generations, n_parents))

    if ggenetic_removed:
        print("\nAlgoritmo genetico, codifica: vettore a {} interi".format(k))

        start_time = time.time()
        genetic_removed = genetic_algo_removed(graph, population, n_parents, max_generations)
        genetic_sol = calc_objective(graph, genetic_removed)
        genetic_alt_sol = calc_alt_objective(graph, genetic_removed)

        calc_time = time.time() - start_time
        
        print_solution(genetic_removed, genetic_sol, genetic_alt_sol, opt, alt_opt, calc_time)

        if ddraw:
            draw.show(genetic_removed)

        print("\n-------------------------------------\n")

    if genetic_binary:
        print("\nAlgoritmo genetico, codifica: vettore binario di {} elementi".format(dim))

        start_time = time.time()
        genetic_bin_removed = genetic_algo_binary(graph, population, n_parents, max_generations)
        genetic_bin_sol = calc_objective(graph, genetic_bin_removed)
        genetic_bin_alt_sol = calc_alt_objective(graph, genetic_bin_removed)

        calc_time = time.time() - start_time
        
        print_solution(genetic_bin_removed, genetic_bin_sol, genetic_bin_alt_sol, opt, alt_opt, calc_time)

        if ddraw:
            draw.show(genetic_bin_removed)

        print("\n-------------------------------------\n")
    
    if save:
        ris = ""
        while ris != "y" and ris != "n":
            ris = input("Salva grafo? [y/n]")
        if ris == "y":
            name = input("Mettice il nome, aooooo: ")
            with open(name, "w+") as f:
                f.write(str(graph))