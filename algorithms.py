#! /usr/bin/env python3

# pylint: disable=missing-module-docstring,missing-function-docstring
# pylint: disable=invalid-name

import collections

def topologicalSortedDepsCoverAndCycles(nodes, edges_func):
    """
    Given a directed graph, find the topologically sorted nodes and if graph
    have cycles then return all cycles.
    @nodes is the list of vertex in the graph. Elements of @nodes should be
        hashable.
    @edges_func(x) return the adjacent list of node x. i.e. return the
        list of nodes y s.t. there is an edge from x -> y.
    """
    visited = set()
    ancestors = set()
    ancestors_stack = []  # To store the exact cycle path.
    topological_sorting = []
    cycles = []
    def runDFS(node):
        ancestors.add(node)
        ancestors_stack.append(node)
        for n in edges_func(node):
            if n not in visited:
                if n in ancestors:  # Cycle found.
                    cycle_path = ancestors_stack[ancestors_stack.index(n):]
                    cycle_path.append(n)
                    cycles.append(cycle_path)
                else:
                    runDFS(n)
        ancestors.remove(node)
        ancestors_stack.pop()
        visited.add(node)
        topological_sorting.append(node)
    for node in nodes:
        if node not in visited:
            runDFS(node)
    return topological_sorting, cycles

def topologicalSortedDepsCover(nodes, edges_func):
    topological_sorting, cycles = topologicalSortedDepsCoverAndCycles(nodes, edges_func)
    assert len(cycles) == 0
    return topological_sorting

def depsCover(nodes, edge_func):
    """
    Given a graph with @nodes and @edge_func (node -> adjacent nodes), compute
    the set of nodes reachable from @nodes.
    """
    q = collections.deque(nodes)
    visited = set(nodes)
    while len(q) > 0:
        q_top = q.pop()
        for i in edge_func(q_top):
            if i not in visited:
                q.appendleft(i)
                visited.add(i)
    return visited

def depsCoverTopo(nodes, edge_func):
    """
    Given a graph with @nodes and @edge_func (node -> adjacent nodes), compute
    the set of nodes reachable from @nodes.
    """
    q = collections.deque(nodes)
    visited = set(nodes)
    while len(q) > 0:
        q_top = q.pop()
        for i in edge_func(q_top):
            if i not in visited:
                q.appendleft(i)
                visited.add(i)
    return visited
