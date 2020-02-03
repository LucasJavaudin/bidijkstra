"""Compare speed of the different implementations of Dijkstra's algorithm.

Author: Lucas Javaudin
E-mail: lucas.javaudin@ens-paris-saclay.fr
"""

from timeit import timeit

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from bidijkstra.bidijkstra_py import dijkstra as dijkstra_python
from bidijkstra.bidijkstra_py_compiled import dijkstra as dijkstra_python_compiled
from bidijkstra.bidijkstra_cython import dijkstra as dijkstra_cython
from bidijkstra.bidijkstra_fibonacci import dijkstra as dijkstra_cython_fibo
from bidijkstra.bidijkstra_openmp import multi_dijkstra as multi_dijkstra_openmp

# Generate a dict containing the name and expression
method_functions = {'Networkx bidirectional': 'nx.bidirectional_dijkstra(G, source, target)',
                  'Python':'dijkstra_python(G, source, target)',
                  'Python Compiled':'dijkstra_python_compiled(G, source, target)',
                  'Cython':'dijkstra_cython(G, source, target)',
                  'Cython Fibonacci':'dijkstra_cython_fibo(G, source,target)'
                  }

# Generate a dict for name and run time
times_methods = {name: list() for name, function in method_functions.items()}
# Add Openmp method
times_methods["Openmp"] = list()

# Range for graph size
start, stop, number = 1, 5, 5
x = np.logspace(start,stop, number)
print(x)
# Number of run for each tested functions.
N = 1

# Fix random seed
np.random.seed(42)

for n in x:
    print(n)
    n = int(n)
    nb_nodes = n
    nb_edges = 4 * n
    # Generate a random directed graph using Networkx.
    in_deg, out_deg = np.random.multinomial(
        n=nb_edges-nb_nodes,
        pvals=np.ones(nb_nodes)/nb_nodes,
        size=2,
    ) + 1
    G = nx.directed_havel_hakimi_graph(in_deg, out_deg)
    # Add random weights to the graph.
    weights = np.random.randint(1, 1000, size=nb_edges)
    for i, (u, v) in enumerate(G.edges()):
        G.edges[u, v]['weight'] = weights[i]

    # Randomly choose a source and a target node.
    M = 10000
    sources = [np.random.choice(G.nodes) for i in range(M)]
    targets = sources.copy()

    for i in range(len(targets)):
        while targets[i] == sources[i]:
            targets[i] = np.random.choice(G.nodes)

    for method, function in method_functions.items():
        t_mean = 0
        for source, target in zip(sources, targets):
            t = timeit(
                function,
                number=N, globals=globals(),
            )
            t /= N
            t_mean += t
        times_methods[method].append(t_mean)

    t_openmp = timeit(
        'multi_dijkstra_openmp(G, sources, targets)',
        number=N, globals=globals(),
    )
    t_openmp /= N
    times_methods["Openmp"].append(t_openmp)

for method, times in times_methods.items():
    plt.plot(np.log(x), times, label=method)
plt.legend()
plt.xlabel('Number of nodes')
plt.ylabel('Time (s)')
plt.title('Comparison of methods for multiple problems')
plt.savefig('plot_parallel_comparison.pdf')
