"""Compare speed of the different implementations of Dijkstra's algorithm.

Author: Lucas Javaudin
E-mail: lucas.javaudin@ens-paris-saclay.fr
"""

from timeit import timeit

import numpy as np
import networkx as nx

from bidijkstra.bidijkstra_py import dijkstra as dijkstra_python
from bidijkstra.bidijkstra_py_compiled import dijkstra as dijkstra_python_compiled
from bidijkstra.bidijkstra_cython import dijkstra as dijkstra_cython
from bidijkstra.bidijkstra_fibonacci import dijkstra as dijkstra_cython_fibo
from bidijkstra.bidijkstra_openmp import dijkstra as dijkstra_openmp

# Generate a dict containing the name and expression
method_functions = {'Networkx bidirectional': 'nx.bidirectional_dijkstra(G, source, target)',
                  'Python':'dijkstra_python(G, source, target)',
                  'Python Compiled':'dijkstra_python_compiled(G, source, target)',
                  'Cython':'dijkstra_cython(G, source, target)',
                  'Cython Fibonacci':'dijkstra_cython_fibo(G, source,target)',
                  'Openmp':'dijkstra_openmp(G, source,target)'
                  }

# Generate a random directed graph using Networkx.
np.random.seed(0)
nb_nodes = 10000
nb_edges = 40000
in_deg, out_deg = np.random.multinomial(
    n=nb_edges-nb_nodes,
    pvals=np.ones(nb_nodes)/nb_nodes,
    size=2,
) + 1
print(in_deg, out_deg)
G = nx.directed_havel_hakimi_graph(in_deg, out_deg)
# Add random weights to the graph.
weights = np.random.randint(1, 1000, size=nb_edges)
for i, (u, v) in enumerate(G.edges()):
    G.edges[u, v]['weight'] = weights[i]

# Randomly choose a source and a target node.
source = np.random.choice(G.nodes)
target = source
while target == source:
    target = np.random.choice(G.nodes)

# Number of run for each tested functions.
N = 10

# import cProfile
# import pstats
# from pstats import SortKey
# cProfile.run('nx.dijkstra_path_length(G, source, target)', "Profile.prof")
# p = pstats.Stats("Profile.prof")
# p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()

# import cProfile
# import pstats
# from pstats import SortKey
# cProfile.run('dijkstra_cython(G, source, target)', "Profile.prof")
# p = pstats.Stats("Profile.prof")
# p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()

# Networkx.

for method, function in method_functions.items():
    l = eval(function)[0]
    t = timeit(
        function,
        number=N, globals=globals(),
    )
    t /= N
    print(f'Found a path of length {l} in {t} seconds using {method}.')

