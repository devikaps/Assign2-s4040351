# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Kruskal's maze generator.
#
# __author__ = Devika Sheeja
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from random import choice
from maze.maze import Maze
from maze.util import Coordinates
import heapq

class KruskalMazeGenerator():
    """
    Kruskal's algorithm maze generator.
    TODO: Complete the implementation (Task A)
    """

    class UnionFind():
        """Disjoint set class to be used for implemeting union-find datastructure

        Psuedocode:
            Step 1: Intiialize the datastructure
                    - set vertices as their parent itself
                    - set the value for each vertex as 0

            Step 2: Find operation definition
                    - find the root of the node
                        (initially it will be the node itself)

            Step 3: Union operation
                    - Set the new parent based on the values
                    - The vertex on the highest level will be the parent
                    - Set the increase the hight of the new parent's level,
                        if the two vertices were at the same level
        """
        def __init__(self, vertices: Coordinates) -> None:
            """Step 1:"""
            self.parent = dict()
            self.level = dict()

            for vertex in vertices:
                # set key as itsemf
                self.parent.update({vertex: vertex})
                self.level.update({vertex: 0})


        def find(self, vertex):
            """Step #2."""
            if self.parent[vertex] != vertex:
                return self.parent[vertex]

            # if parent is the vertex (inital case)
            return vertex

        def union(self, vertex1, vertex2):
            """Step #3."""
            parent1 = self.find(vertex1)
            parent2 = self.find(vertex2)

            if parent1 == parent2: return

            # Setting the new parennt
            if self.level[parent1] < self.level[parent2]:
                self.parent[parent1] = parent2
            elif self.level[parent1] > self.level[parent2]:
                self.parent[parent2] = parent1
            else:
                self.parent[parent2] =  parent1
                # with new child added, increse the level of the parent
                self.level[parent1] += 1

    class Edge:
        """Edge class to define a node to be used in heap
            Here,
                - edge => maze.edge
                - weigth => maze.edgeWeight
        """
        def __init__(self, edge, weight:int) -> None:
            self.edge = edge
            self.weight = weight

        def __lt__(self, edge):
            return self.weight < edge.weight

    def generateMaze(self, maze:Maze):
        """
        Kruskal algorithm works by picking the shortest spanning tree.

        PseudoCode:
            1. Fetch the max iterations (No.Of vertieces-1)
            2. Keep the edges in a heapq.
               This will help in reducing the complexity.
            3. for each edge.
            4.     fetch the edge with lowest cost.
            5.     add to the spanning tree if no cycle forms.

        Datastructures Used:
            - min-heap
            - union-find

        Time complexity:
            V(log E) -> for V - vertices & E - Edges

        """
        # TODO: Implement this method for task A.

        # step 1: Fetch the max iterations (No.Of vertieces-1)
        iterations = len(maze.getCoords()) - 1
        min_span_tree = list()

        # step 2: Keep the edges in a heapq
        edges = list()
        heapq.heapify(edges)
        for edge in maze.getEdges():
            node = self.Edge(edge,maze.edgeWeight(edge[0],edge[1]))
            heapq.heappush(edges, node)

        # step 3
        unionFind = self.UnionFind(maze.getCoords())
        while iterations > 0 and edges:
            # step 4
            smallest_edge = heapq.heappop(edges)
            # print(f"Choosing edge {smallest_edge}")

            selected_edge = smallest_edge.edge
            vertex1 = selected_edge[0]
            vertex2 = selected_edge[1]

            # step 5
            # expand min-span_tree if the new edge will not form a cycle
            if unionFind.find(vertex1) != unionFind.find(vertex2):
                # merge the parents to find the cycle later
                unionFind.union(unionFind.find(vertex1),
                                unionFind.find(vertex2))

                min_span_tree.append(selected_edge)

                # remove wall if it exists
                maze.removeWall(vertex1,vertex2)

            # Mark completion for one iteration
            iterations -= 1
