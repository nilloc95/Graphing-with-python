# Course: CS261 - Data Structures
# Author: Collin Gilmore
# Assignment: 6
# Description:  This file contains a class for an undirected graph using a dictionary with a list for each key
#               to store links between nodes. It also has methods to add vertices, edges, remove vertices and edges,
#               find out if a path is valid, depth and breadth first searches, the number of components in the graph
#               and if the graph contains a cycle or not

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        if v not in self.adj_list:
            self.adj_list[v] = []
        if u not in self.adj_list:
            self.adj_list[u] = []
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)
            self.adj_list[v].sort()
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
            self.adj_list[u].sort()

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if v not in self.adj_list or u not in self.adj_list:
            return
        if v in self.adj_list[u] and u in self.adj_list[v]:
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v in self.adj_list:
            del self.adj_list[v]

            for vertex in self.adj_list.items():
                if v in vertex[1]:
                    vertex[1].remove(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vertices = []
        for vertex in self.adj_list:
            vertices.append(vertex)

        return vertices

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edges = []
        for edge in self.adj_list.items():
            if len(edge[1]) != 0:
                for vertex in edge[1]:
                    if (edge[0], vertex) not in edges and (vertex, edge[0]) not in edges:
                        edges.append((edge[0], vertex))

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """

        length = len(path)

        if length == 0:
            return True

        if length == 1:
            for edges in self.adj_list.values():
                if path[0] in edges:
                    return True
            return False

        for i in range(length - 1):
            if path[i] not in self.adj_list:
                return False
            if path[i + 1] not in self.adj_list[path[i]]:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        path = []
        stack = []

        # Return empty path if the start isn't in the graph
        if v_start not in self.adj_list:
            return path

        # Else: Search the entire graph until we've searched everything or the value is found. Return the search path
        path.append(v_start)
        for vertex in reversed(self.adj_list[v_start]):
            stack.append(vertex)

        if v_end in path:
            return path

        while len(stack) != 0:
            current = stack.pop()
            if current not in path:
                path.append(current)

            if current == v_end:
                return path

            for vertex in reversed(self.adj_list[current]):
                if vertex not in path:
                    stack.append(vertex)

        return path

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        path = []
        queue = deque()

        # Return empty path if the start isn't in the graph
        if v_start not in self.adj_list:
            return path

        # Else: Search the entire graph until we've searched everything or the value is found. Return the search path
        path.append(v_start)
        for vertex in self.adj_list[v_start]:
            queue.append(vertex)

        if v_end in path:
            return path

        while len(queue) != 0:
            current = queue.popleft()
            if current not in path:
                path.append(current)

            if current == v_end:
                return path

            for vertex in self.adj_list[current]:
                if vertex not in path:
                    queue.append(vertex)

        return path

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        components = 1
        path = self.dfs(next(iter(self.adj_list)))

        for item in self.adj_list:
            if item not in path:
                path += self.dfs(item)
                components += 1

        return components

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        parents = []
        path = []
        stack = []

        v_start = next(iter(self.adj_list))

        path.append(v_start)
        for vertex in reversed(self.adj_list[v_start]):
            parents.append(v_start)
            stack.append(vertex)
        current = v_start

        if self.cycle_helper(current, path, stack, parents):
            return True

        for item in self.adj_list:
            if item not in path:
                for vertex in reversed(self.adj_list[item]):
                    parents.append(item)
                    stack.append(vertex)
                current = item
                if self.cycle_helper(current, path, stack, parents):
                    return True

        return False

    def cycle_helper(self, current, path, stack, parents):
        """
        Helper method for has_cycle so that an iterative approach can be used
        """
        while len(stack) != 0:
            current = stack.pop()
            parent = parents.pop()

            if current not in path:
                path.append(current)

            for vertex in reversed(self.adj_list[current]):
                if vertex not in path and vertex not in stack:
                    stack.append(vertex)
                    parents.append(current)
                if vertex in path and vertex != parent:
                    return True

        return False

if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = UndirectedGraph()
    # print(g)
    #
    # for v in 'ABCDE':
    #     g.add_vertex(v)
    # print(g)
    #
    # g.add_vertex('A')
    # print(g)
    #
    # for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #     g.add_edge(u, v)
    # print(g)

    #
    # print("\nPDF - method remove_edge() / remove_vertex example 1")
    # print("----------------------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # g.remove_vertex('DOES NOT EXIST')
    # g.remove_edge('A', 'B')
    # g.remove_edge('X', 'B')
    # print(g)
    # g.remove_vertex('D')
    # print(g)
    # #
    #
    # print("\nPDF - method get_vertices() / get_edges() example 1")
    # print("---------------------------------------------------")
    # g = UndirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    #
    # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    # for path in test_cases:
    #     print(list(path), g.is_valid_path(list(path)))

    #
    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # for case in test_cases:
    #     print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    # print('-----')
    # for i in range(1, len(test_cases)):
    #     v1, v2 = test_cases[i], test_cases[-1 - i]
    #     print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')
    #

    # print("\nPDF - method count_connected_components() example 1")
    # print("---------------------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print(g.count_connected_components(), end=' ')
    # print()

    #

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())

    # edges = ['BG', 'DF', 'FH', 'HA', 'IC', 'CJ', 'AK']
    # g = UndirectedGraph(edges)
    # # test_cases = (
    # #     'add QH')
    # # for case in test_cases:
    # #     command, edge = case.split()
    # #     u, v = edge
    # #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    # print(g, g.has_cycle())


