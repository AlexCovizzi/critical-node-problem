import random
from graphdraw import GraphDraw
from greedy import *
from graph import *
from asp import *
from neighbor_search import *
from genetic_algo import *


if __name__ == '__main__':
    graph = create_graph(50, threshold=93, connected=False)

    print("Inizio: " + str(calc_objective(graph, [])))

    k = 6
    
    opt, opt_removed = global_optimum(graph, k)
    
    print("Global optimum")
    print(opt)
    opt_removed.sort()
    print(opt_removed)
    

    bests = [max_degree_best, min_conn_best, min_conn_ratio_best]

    population = create_population(graph, k, 20, bests, 5)

    removed_tabu = algo_greedy(graph, k, min_conn_ratio_best)
    removed = genetic_algo_removed(graph, population, n_parents=8, max_generations=100)
    
    print("Genetic removed optimum")
    print(calc_objective(graph, removed))
    print("In pop: "+ str(removed in population))
    removed.sort()
    print(removed)

    input()
    
    removed_binary = genetic_algo_binary(graph, population, n_parents=8, max_generations=100)

    print("\nGenetic removed binary")
    print(calc_objective(graph, removed_binary))
    print("In pop: "+ str(removed_binary in population))
    removed_binary.sort()
    print(removed_binary)
    print(str(removed) == str(removed_binary))

    '''
    while True:
        best_1_swap(graph, removed)
        sol = calc_objective(graph, removed)
        if sol > best:
            best = sol
        else:
            break
    '''
    
    input()
    
    best_tabu_initial = calc_objective(graph, removed_tabu)
    tabu_search(graph, removed_tabu, n_stall=100)
    best_tabu = calc_objective(graph, removed_tabu)
    
    print("\n------------------------------\n")

    print(best_tabu_initial)
    print("tabu")
    print(best_tabu)
    removed_tabu.sort()
    print(removed_tabu)
