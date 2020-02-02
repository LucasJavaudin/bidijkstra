# distutils: language = c++
# cython: language_level = 3
"""Cython implementation of bidirectional Dijkstra with C++ priority queue and
parallelization with OpenMP.

Author: Lucas Javaudin
E-mail: lucas.javaudin@ens-paris-saclay.fr
"""
from libcpp.utility cimport pair
from libcpp.map cimport map
from libcpp.vector cimport vector
from libcpp.queue cimport priority_queue

from cython.parallel import prange

cimport cython

import numpy as np

def multi_dijkstra(G, vector[int] sources, vector[int] targets,
                   weight='weight'):

    assert sources.size() == targets.size(), \
        'Sources and targets lists should have same size.'

    cdef (int, vector[int]) results

    n = sources.size()
    cdef vector[int] dists
    cdef vector[vector[int]] paths

    cdef int i
    if n == 1:
        results = cdijkstra(G, sources[0], targets[0], weight)
        dists.push_back(results[0])
        paths.push_back(results[1])
    else:
        for i in prange(n, nogil=True):
            results = cdijkstra(G, sources[i], targets[i], weight)
            with gil:
                dists.push_back(results[0])
                paths.push_back(results[1])

    return dists, paths

def dijkstra(G, source, target, weight='weight'):
    return cdijkstra(G, source, target, weight)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef (int, vector[int]) cdijkstra(G, int source, int target, weight='weight') nogil:

    # Adjacency matrix for forward and backward search.
    with gil:
        adjacency = [G._succ, G._pred]

    cdef map[int, int] results0, results1
    cdef priority_queue[pair[int, int]] fringe0, fringe1
    cdef map[int, int] seen0, seen1
    # Store shortest paths for each node in both directions.
    cdef map[int, vector[int]] paths0, paths1
    paths0[source].push_back(source)
    paths0[target].push_back(target)

    cdef pair[int, int] p
    cdef pair[int, int] push_pair;

    seen0[source] = 0
    seen1[target] = 0
    push_pair.first = 0
    push_pair.second = source
    fringe0.push(push_pair)
    push_pair.second = target
    fringe1.push(push_pair)

    cdef int best_dist = 0
    cdef vector[int] best_path0, best_path1, best_path

    # Search direction (0 for forward, 1 for backward).
    cdef bint d = 1

    cdef int alt_dist, dist, out_node, path_dist
    cdef vector[int] out_nodes, dists
    cdef int i, n

    while not fringe0.empty() and not fringe1.empty():
        # Change direction.
        d = 1 - d

        # Find next closest node.
        if d:
            p = fringe1.top()
            fringe1.pop()
        else:
            p = fringe0.top()
            fringe0.pop()

        if d:
            if results1.find(p.second) != results1.end():
                # Node already reached.
                continue
            results1[p.second] = -p.first
            # Check if the node has already been reached in the other
            # direction.
            if results0.find(p.second) != results0.end():
                break
        else:
            if results0.find(p.second) != results0.end():
                # Node already reached.
                continue
            results0[p.second] = -p.first
            # Check if the node has already been reached in the other
            # direction.
            if results1.find(p.second) != results1.end():
                break

        # Find outgoing nodes in the adjacency matrix and put the id and
        # distance in C++ vectors (this allows Cython to compute next loop
        # efficiently).
        out_nodes.clear()
        dists.clear()
        with gil:
            for node, attributes in adjacency[d][p.second].items():
                out_nodes.push_back(node)
                dists.push_back(attributes[weight])

        n = out_nodes.size()

        for i in range(n):
            out_node = out_nodes[i]
            dist = dists[i]
            alt_dist = -p.first + dist
            if (
                d and ( seen1.find(out_node) == seen1.end()
                       or alt_dist < seen1[out_node] )
                or not d and ( seen0.find(out_node) == seen0.end()
                              or alt_dist < seen0[out_node] )
            ):
                if d:
                    seen1[out_node] = alt_dist
                    push_pair.first = -alt_dist
                    push_pair.second = out_node
                    fringe1.push(push_pair)
                else:
                    seen0[out_node] = alt_dist
                    push_pair.first = -alt_dist
                    push_pair.second = out_node
                    fringe0.push(push_pair)
                # The path to out_node is the path to the previous node plus
                # out_node.
                if d:
                    paths1[out_node] = paths1[p.second]
                    paths1[out_node].push_back(out_node)
                else:
                    paths0[out_node] = paths0[p.second]
                    paths0[out_node].push_back(out_node)
                if ( seen0.find(out_node) != seen0.end()
                        and seen1.find(out_node) != seen1.end() ):
                    # Potential path found.
                    path_dist = seen0[out_node] + seen1[out_node]
                    if best_path0.size() == 0 or path_dist < best_dist:
                        best_dist = path_dist
                        best_path0 = paths0[out_node]
                        best_path1 = paths1[out_node]

    with gil:
        revpath = list(best_path1)
        revpath.reverse()
        best_path = list(best_path0) + revpath[1:]

    return best_dist, best_path
