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
from student.lib import build_wall_heap
from student.lib import UnionFind
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

    def generateMaze(self, maze:Maze):
        """
        Kruskal algorithm works by picking the shortest spanning tree.

        PseudoCode:
            1. Fetch the max iterations (No.Of vertieces-1)
            2. Keep the edges in a heapq. This will help in reducing th complexity.
            3. for each wall.
            4.     fetch the wall with lowest cost towards entrance.
            5.     add to the spanning tree to find out if no cycle forms.
            6.     remove the wall

        Datastructures Used:
            - min-heap
            - union-find

        Time complexity:
            V(log W) -> for V - vertices & W - Walls

        """
        # TODO: Implement this method for task A.

        total_vertices = len(maze.getCoords())          # step 1: Fetch the max iterations (No.Of vertieces-1)
        min_span_tree = list()
        walls = build_wall_heap(maze)                   # step 2: Keep the edges in a heapq with entrances

        unionFind = UnionFind(maze.getCoords())
        while len(min_span_tree) < total_vertices - 1 and walls:
            curr_wall = heapq.heappop(walls)            # step 4: fetch the wall with lowest cost towards entrance.
            selected_wall = curr_wall.node
            vertex1 = selected_wall[0]
            vertex2 = selected_wall[1]

            if unionFind.union(vertex1, vertex2):       # checking if removing the wall will merge two disjoint sets
                min_span_tree.append(selected_wall)     # and if it doesnt form a cycle
                maze.removeWall(vertex1,vertex2)        # remove wall if it is the shortest path towards exits
