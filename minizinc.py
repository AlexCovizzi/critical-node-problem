import subprocess
import sys
import json


def print_minizinc(graph, k, out="problema.mzn"):
    """
    int: n = 6;
    int: k = 2;
    array[1..n,1..n] of int: E =[| 0, 1, 0, 0, 1, 1
    | 1, 0, 0, 1, 0, 1
    | 0, 0, 0, 1, 1, 1
    | 0, 1, 1, 0, 0, 1
    | 1, 0, 1, 0, 0, 0
    | 1, 1, 1, 1, 0, 0 |];
    """
    with open(out, "w") as f:
        f.write("int: n = {};\n".format(len(graph)))
        f.write("int: k = {};\n".format(k))
        f.write("array[1..n, 1..n] of int: E = ")
        f.write("[")
        for i in range(len(graph)):
            row = graph[i]
            f.write("| " + ",".join(str(v) for v in row))
        f.write("|];\n")

        with open("critical-node.mzn", "r") as model:
            text = model.read()
            f.write(text)


def relaxed_optimum(graph, k, mzn_name="problema.mzn"):
    print_minizinc(graph, k, mzn_name)

    mzn_output = subprocess.run(['minizinc', '--solver', 'osicbc', mzn_name], stdout=subprocess.PIPE).stdout.decode('utf-8')
    with open("mzn-output", "w") as f:
        f.write(mzn_output)
    
    with open("mzn-output", "r") as f:
        first_line = f.readline()
        if sys.platform.startswith('win'):
            f.readline()
        second_line = f.readline()
        removed = json.loads(first_line)
        threshold = (len(graph) - len([r for r in removed if r > 0]) - k) / len(graph)
        removed = [i for i,v in enumerate(removed) if v > 0]
        sol = float(second_line)
    
    return sol, removed