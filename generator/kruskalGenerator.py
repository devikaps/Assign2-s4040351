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

    # Defined two classes
    #     - UnionFind() - implements union-find datastructure
    #     - Edge()  - to represent a node in the min-span-tree heap
    #     - build_wall_heap - to keep the walls and its weight in heap
    #                         as heap serves the purpose of retrieving the smallest wall

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

            for vertex in vertices:
                # set key as itsemf
                self.parent.update({vertex: vertex})


        def find(self, vertex):
            """Step #2."""
            if self.parent[vertex] != vertex:
                return self.find(self.parent[vertex])

            # if parent is the vertex (inital case)
            return vertex

        def union(self, vertex1, vertex2):
            """Step #3."""
            parent1 = self.find(vertex1)
            parent2 = self.find(vertex2)

            if parent1 == parent2: return False

            # Setting the new parent
            self.parent[parent1] = parent2
            return True

    class Edge:
        """Edge class to define a node to be used in heap
            Here,
                - edge => maze.edge
                - weigth => maze.edgeWeight
        """
        def __init__(self, node, weight:int) -> None:
            self.node = node
            self.weight = weight

        def __lt__(self, node):
            return self.weight < node.weight


    def build_wall_heap(self, maze) ->list():
        """Building heap with edges and their weights"""
        edges = list()
        heapq.heapify(edges)

        for edge in maze.getEdges():
            if maze.hasWall(edge[0], edge[1]):
                distance = maze.edgeWeight(edge[0],edge[1])
                node = self.Edge(edge,distance)
                heapq.heappush(edges, node)

        return edges

    def generateMaze(self, maze:Maze):
        """
        Kruskal algorithm works by picking the shortest spanning tree.

        PseudoCode:
            1. Fetch the max iterations (No.Of vertieces-1)
            2. Keep the edges in a heapq.
               This will help in reducing th complexity.
            3. for each wall.
            4.     fetch the wall with lowest cost towards entrance.
            5.     add to the spanning tree if no cycle forms.
            6.     remove the wall
        Datastructures Used:
            - min-heap
            - union-find

        Time complexity:
            V(log W) -> for V - vertices & W - Walls

        """
        # TODO: Implement this method for task A.

        # step 1: Fetch the max iterations (No.Of vertieces-1)
        total_vertices = len(maze.getCoords())
        min_span_tree = list()

        # print(maze.getEntrances())
        # step 2: Keep the edges in a heapq with entrances
        walls = self.build_wall_heap(maze)

        # step 3
        unionFind = self.UnionFind(maze.getCoords())
        while len(min_span_tree) < total_vertices - 1 and walls:
            # step 4
            curr_wall = heapq.heappop(walls)
            selected_wall = curr_wall.node
            vertex1 = selected_wall[0]
            vertex2 = selected_wall[1]

            # checking if removing the wall will merge two disjoint sets
            if unionFind.union(vertex1, vertex2):
                min_span_tree.append(selected_wall)
                # remove wall if it is the shortest path towards exits
                maze.removeWall(vertex1,vertex2)
