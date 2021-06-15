# Course: CS261 - Data Structures
# Author: Collin Gilmore
# Assignment: 6
# Description:  This file contains a class for an directed graph using a matrix to store links between nodes
#               along with the weight. It also has methods to add vertices, edges, remove edges,
#               find out if a path is valid, depth and breadth first searches, if the graph contains a cycle or not,
#               and dijkstra's algorithm to find the shortest path to each node

from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Add new vertex to the graph
        """
        self.adj_matrix.append([0 for x in self.adj_matrix])
        for vertex in self.adj_matrix:
            vertex.append(0)
        self.v_count += 1
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add edge to the graph
        """
        if weight < 1:
            return
        if src == dst:
            return
        if src >= self.v_count or dst >= self.v_count:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes and edge between two vertices, if they are in the correct range
        """
        if src < 0 or dst < 0:
            return
        if src < self.v_count and dst < self.v_count:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        returns the vertices in the graph in a list
        """
        return [x for x in range(self.v_count)]

    def get_edges(self) -> []:
        """
        Returns a list of all the edges
        """
        edges = []

        for x in range(self.v_count):
            for i in range(self.v_count):
                if self.adj_matrix[x][i] != 0:
                    tup = (x, i, self.adj_matrix[x][i])
                    edges.append(tup)

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        length = len(path)

        if length == 0:
            return True

        for i in range(length - 1):
            if path[i] >= self.v_count:
                return False
            if self.adj_matrix[path[i]][path[i + 1]] == 0:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in ascending order
        """
        path = []
        stack = []

        # Return empty path if the start isn't in the graph
        if v_start >= self.v_count:
            return path

        # Else: Search the entire graph until we've searched everything or the value is found. Return the search path
        path.append(v_start)
        for vertex in range(self.v_count - 1, -1, -1):
            if self.adj_matrix[v_start][vertex] != 0:
                stack.append(vertex)

        if v_end in path:
            return path

        while len(stack) != 0:
            current = stack.pop()
            if current not in path:
                path.append(current)

            if current == v_end:
                return path

            for vertex in range(self.v_count - 1, -1, -1):
                if self.adj_matrix[current][vertex] != 0 and vertex not in path:
                    stack.append(vertex)

        return path

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in ascending order
        """
        path = []
        queue = deque()

        # Return empty path if the start isn't in the graph
        if v_start >= self.v_count:
            return path

        # Else: Search the entire graph until we've searched everything or the value is found. Return the search path
        path.append(v_start)
        for vertex in range(self.v_count):
            if self.adj_matrix[v_start][vertex] != 0:
                queue.append(vertex)

        if v_end in path:
            return path

        while len(queue) != 0:
            current = queue.popleft()
            if current not in path:
                path.append(current)

            if current == v_end:
                return path

            for vertex in range(self.v_count):
                if self.adj_matrix[current][vertex] != 0 and vertex not in path:
                    queue.append(vertex)

        return path

    def has_cycle(self):
        """
        Returns True if there is a cycle in the directed graph, returns False otherwise
        """
        visited = [False for x in range(self.v_count)]
        found = False

        for vertex in range(self.v_count):
            visited[vertex] = True
            for link in range(self.v_count - 1, -1, -1):
                if self.adj_matrix[vertex][link] != 0:
                    found = self.cycle_helper(visited, link)
                    if found is True:
                        return True
            visited[vertex] = False

        return False

    def cycle_helper(self, visited, current):
        """
        Helper method for has_cycle used recursively
        """
        if visited[current] is True:
            return True

        visited[current] = True
        found = False

        for i in range(self.v_count - 1, -1, -1):
            if self.adj_matrix[current][i] != 0:
                found = self.cycle_helper(visited, i)
                if found is True:
                    return True
        visited[current] = False
        return False

    def dijkstra(self, src: int) -> []:
        """
        Takes a starting vertex and returns a list with the shortest path to all other vertices in the graph. A vertex
        will contain an "inf" value if it cannot be reached.
        """
        length = len(self.adj_matrix)
        output = [float('inf') for x in range(length)]
        output[src] = 0
        finished = [False for x in range(length)]

        for vertex in range(length):
            low = self.minDistance(output, finished)

            if low is None:
                return output

            finished[low] = True

            for index in range(length):
                if self.adj_matrix[low][index] > 0 and finished[index] is False and \
                        output[index] > output[low] + self.adj_matrix[low][index]:
                    output[index] = output[low] + self.adj_matrix[low][index]
        return output

    def minDistance(self, lengths, processed):
        """Helper function for dijkstra's algorithm to find the next shortest node"""
        minimum = float('inf')
        index = None

        for vertex in range(len(self.adj_matrix)):
            if lengths[vertex] < minimum and processed[vertex] is False:
                minimum = lengths[vertex]
                index = vertex

        return index


if __name__ == '__main__':
    #
    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)
    #
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)

    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')

    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))

    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')
    #
    # print("\nPDF - method dfs() and bfs() example 2")
    # print("--------------------------------------")
    # edges = [(2, 11, 7), (3, 8, 13), (4, 7, 1), (4, 4, 10), (6, 3, 7), (6, 11, 7), (10, 4, 14), (11, 5, 2), (11, 12, 9),
    #          (12, 4, 4), (12, 6, 5)]
    # g = DirectedGraph(edges)
    #
    # print(f'DFS:{g.dfs(12)} BFS:{g.bfs(6)}')

    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    #
    # edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    # for src, dst in edges_to_remove:
    #     g.remove_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    #
    # edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    # for src, dst in edges_to_add:
    #     g.add_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    # print('\n', g)
    #
    # print("\nPDF - method has_cycle() example 2")
    # print("----------------------------------")
    # edges = [(0, 3, 1), (2, 6, 17), (2, 8, 14), (3, 11, 7), (4, 5, 19), (5, 3, 19), (5, 10, 2), (5, 11, 10), (6, 7, 15),
    #          (8, 6, 15), (8, 12, 7), (11, 7, 20), (12, 9, 10)]
    # g = DirectedGraph(edges)
    #
    # print(g.get_edges())
    # print(g.has_cycle())
    # print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
