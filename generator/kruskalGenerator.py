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

    # Defined two classes
    #     - UnionFind() - implements union-find datastructure
    #     - Edge()  - to represent a node in the min-span-tree heap
    #     - build_wall - to keep the walls and its weight in heap
    #                    as heap serves the purpose of retrieving the smallest wall

    def generateMaze(self, maze:Maze):
        """
        Kruskal algorithm works by picking the shortest spanning tree.

        PseudoCode:
            1. Fetch the walls and sort it based on the edge weight
            2. Keep the edges in a heapq. This will help in reducing th complexity.
            3. for each wall.
            4.     fetch the wall with lowest cost towards entrance.
            5.     add to the spanning tree to find out if no cycle forms.
            6.     remove the wall when the union function returns true (when no cycle is formed with this merge)

        Datastructures Used:
            - union-find

        Time complexity:
            V(log W) -> for V - vertices & W - Walls

        """
        # TODO: Implement this method for task A.
        min_span_tree = list()
        walls = get_walls(maze)                        # step 2: fetch the sorted walls with their weights

        unionFind = UnionFind(maze.getCoords())
        for curr_wall in walls:
            selected_wall = curr_wall[0]
            vertex1 = selected_wall[0]
            vertex2 = selected_wall[1]

            if unionFind.union(vertex1, vertex2):       # checking if removing the wall will merge two disjoint sets
                min_span_tree.append(selected_wall)     # and if it doesnt form a cycle
                maze.removeWall(vertex1,vertex2)        # remove wall if it is the shortest path towards exits
