import subprocess
import sys


def print_asp(graph, rem, out="problema.pl"):
    with open(out, "w") as f:
        for i in range(len(graph)):
            f.write("nodo(" + str(i) + ")." + "\n")
        
        for i in range(len(graph)):
            for j in range(i + 1, len(graph)):
                if graph[i][j] == 1:
                    f.write("arco(" + str(i) + ", " + str(j) + ")." + "\n")
        
        f.write("rem(" + str(rem) + ").")

        with open("critical-node.pl", "r") as model:
            text = model.read()
            f.write(text)


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