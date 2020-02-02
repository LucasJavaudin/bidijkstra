"""Pure Python implementation of bidirectional Dijkstra.

Author: Lucas Javaudin
E-mail: lucas.javaudin@ens-paris-saclay.fr
"""

import numpy as np

from heapq import heappush, heappop

def dijkstra(G, source, target, weight='weight'):

    # Adjacency matrix for forward and backward search.
    adjacency = [G._succ, G._pred]

    results = [dict(), dict()]
    fringe = [list(), list()]
    seen = [dict(), dict()]
    # Store shortest paths for each node in both directions.
    paths = [
        {source: [source]},
        {target: [target]}
    ]

    seen[0][source] = 0
    seen[1][target] = 0
    heappush(fringe[0], (0, source))
    heappush(fringe[1], (0, target))

    best_dist = np.inf
    best_path = None

    # Search direction (0 for forward, 1 for backward).
    d = 1

    while fringe[0] and fringe[1]:
        # Change direction.
        d = int(not d)

        # Find next closest node.
        (min_dist, min_node) = heappop(fringe[d])

        if min_node in results[d]:
            continue

        results[d][min_node] = min_dist

        # Check if the node has already been reached in the other direction.
        if min_node in results[int(not d)]:
            break

        for out_node, attributes in adjacency[d][min_node].items():
            dist = attributes[weight]
            alt_dist = min_dist + dist
            if out_node not in seen[d] or alt_dist < seen[d][out_node]:
                seen[d][out_node] = alt_dist
                heappush(fringe[d], (alt_dist, out_node))
                # The path to out_node is the path to the previous node plus
                # out_node.
                paths[d][out_node] = paths[d][min_node] + [out_node]
                if out_node in seen[0] and out_node in seen[1]:
                    # Potential path found.
                    path_dist = seen[0][out_node] + seen[1][out_node]
                    if path_dist < best_dist:
                        best_dist = path_dist
                        revpath = paths[1][out_node][:]
                        revpath.reverse()
                        best_path = paths[0][out_node] + revpath[1:]

    return best_dist, best_path
