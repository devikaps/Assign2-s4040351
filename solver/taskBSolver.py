# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Brute force maze solver for all entrance, exit pairs
#
# __author__ = Devika Sheeja
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze

from typing import List
from solver.recurBackMazeSolver import RecurBackMazeSolver
from student.lib import Node


class bruteForceSolver():

    def __init__(self):
        # TODO: Implement this for task B!
        self.all_solved = False
        self.entrance_exit_paths = dict()

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]):
        # TODO: Implement this for task B!
        """Solver Maze logic:
        Step 1: fetch path from entrance at index 0 to exit index 0
        Steo 2: fetch and find a path from the entrance and exit index 1
        Step 3: return all_solved flag as true if the second path also exits
        """

        entrance_index = 0
        self.entrance_exit_paths.update({entrance_index: self.findPath(maze, entrances, exits, [], entrance_index)})

        if self.entrance_exit_paths:
            entrance_index += 1
            self.entrance_exit_paths.update({entrance_index: self.findPath(maze, entrances, exits, self.entrance_exit_paths[0], entrance_index)})
            self.all_solved = len(self.entrance_exit_paths[entrance_index]) > 1

    def getSolverPath(self) -> dict:
        return self.entrance_exit_paths

    def findPath(self, maze: Maze, entrances: Coordinates, exits: List[Coordinates], exclude_list: List[Coordinates], entrance_index: int):
        """This function implements the greedy algorithm dijkshara

        Pseudocode
        ----------
        /*Brute Force Algorithm to find shorted path from an entrance point to exit point
          Input:
                maze - Class that provides the maze related details, including edge, edge-weight, walls, etc
                entrances - an array where the entrances are provided
                exits - an array where the exits are provided
                exclude_path - Nodes to be excluded when finding the path
                index - index of the entrance and exit for which the path to be found
          Output:
                Returns True if a path is found else False
                Also, ammends the path in the dictionary at the index of self.entrance_exit_paths
        */

        Steps:
        ------
        1. Initialize stack N = [ENTRANCE[INDEX]]
        2. Set V = EMPTY_LIST
        3. while N not EMPTY do
        4.      set NODE = N.pop()   > get the shortest path node
        5.      V.PUSH(NODE)         > update visited nodes
        6.      if NODE == EXIT[INDEX] then
        7.          set solved path by traversing V
        8.          return True if PATH_LEVEL > 1
        9.      find nearest non-visited, not in "exclude_list"
        10.     N.push(NEIGHBOUR)
        11. end while
        12. return False


        Datastructures Used:
            - min-heap

        Time complexity:
            E(log V) -> for V - vertices & E - Edges

        """
        stack = [Node(entrances[entrance_index],0)]                      # initialize the processing stack with entrance node
        visited = dict()                                        # empty the visited list
        while stack:
            selected =  stack.pop()                             # FIFO order fetch for next node
            visited.update({selected.node : selected})          # Add the processing node to visited list

            if selected.node == exits[entrance_index]:                   # if the node is the expected exit
                path = selected.node
                m_solverPath = list()
                while path:                                     # process until no parent's found
                    m_solverPath.append(path)                   # add node to the solved path
                    path = visited[path].parent                 # fetch the node's parent

                m_solverPath.reverse()                          # reverse the list as the exit is pushed first and entrance at the end
                return m_solverPath                          # return TRUE if there is a path with atleast 2 nodes


            neighbours = maze.neighbours(selected.node)         # Find neighbours that are NON-VISITED, NOT_EXPLORED, NOT_A_WALL
            nonExploredNeighs = [(neigh, maze.edgeWeight(selected.node, neigh)) for neigh in neighbours if not maze.hasWall(selected.node, neigh) and neigh not in exclude_list and neigh not in visited]
            nonExploredNeighsSorted = sorted(nonExploredNeighs, key = lambda x:x[1]) if nonExploredNeighs else []

            for neigh, distance in nonExploredNeighsSorted:         # process the nodes in their distance order
                neigh_node = Node(neigh, distance, selected.node)
                stack.append(neigh_node)                            # push the nearest node fist for processing

        return []                                                # report No path found by returning False
