"""This is a common library created for the re-use of common classes
    As Confirmed with Ms. Elham.
"""

from maze.maze import Maze
from maze.util import Coordinates
import heapq

def is_boundary(cell:Coordinates, maze:Maze):
    if (cell.getRow() >= 0 and cell.getRow() < maze.rowNum() and cell.getCol() >= 0 and cell.getCol() < maze.colNum()):
        return False # not a boundary
    return True # a boundary

def build_wall_heap(maze: Maze) ->list():
    """Building heap with edges and their weights"""
    edges = list()
    heapq.heapify(edges)

    # parse all edges that has wall and not a boundary to process
    for edge in maze.getEdges():
        if maze.hasWall(edge[0], edge[1]) and not is_boundary(edge[0], maze) and not is_boundary(edge[1], maze):
            distance = maze.edgeWeight(edge[0],edge[1])
            node = Edge(edge,distance)
            heapq.heappush(edges, node)

    return edges


def manhattanHeuristics( xy1:Coordinates, xy2:Coordinates):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1.getRow() - xy2.getRow()) + abs(xy1.getCol() - xy2.getCol())


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


class Node:
    """Node Object defining a node with its distance from starting point"""
    def __init__(self, node, distance, parent=None):
        self.node = node
        self.distance = distance
        self.parent = parent

    def __lt__(self, node):
        return self.distance < node.distance


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
