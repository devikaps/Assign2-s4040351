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
from generator.lib import get_walls
from generator.lib import UnionFind

class KruskalMazeGenerator():
    """
    Kruskal's algorithm maze generator.
    TODO: Complete the implementation (Task A)
    """

    # Defined two classes   [ Please see file: generator/lib.py ]
    #                                         ------------------
    #     - UnionFind() - implements union-find datastructure
    #     - Edge()  - to represent a node in the min-span-tree heap
    #     - build_wall - to keep the walls and its weight in heap
    #                    as heap serves the purpose of retrieving the smallest wall

    def generateMaze(self, maze:Maze):
        """
        Kruskal algorithm work towards finding the shortest spanning tree.

        Logic:
            1. Fetch the walls and sort it based on the edge weight
            2. for each wall.
            3.     fetch the wall with lowest cost towards entrance.
            4.     add to the spanning tree to find out if no cycle forms.
            5.     remove the wall when the union function returns true (when no cycle is formed with this merge)

        Datastructures Used:
            - union-find

        Time complexity:
            O(W) - W: Walls

        """
        # TODO: Implement this method for task A.
        walls = get_walls(maze)                         # step 2: fetch the sorted walls with their weights

        unionFind = UnionFind(maze.getCoords())
        for curr_wall in walls:                         # parse through sorted walls list
            selected_wall = curr_wall[0]                # fetch first shortest node
            vertex1 = selected_wall[0]                  # coordinate(vertices) of edges
            vertex2 = selected_wall[1]

            if unionFind.union(vertex1, vertex2):       # checking if removing the wall will merge two disjoint sets
                maze.removeWall(vertex1,vertex2)        # remove wall as it joins two different sectors
