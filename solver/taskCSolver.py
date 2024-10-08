# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Greedy maze solver for all entrance, exit pairs
#
# __author__ = Devika Sheeja
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze

from typing import List
from solver.dijkstraSolver import DijkstraSolver
from student.lib import Node
from student.lib import heapq
from student.lib import manhattanHeuristics

class greedySolver():

    def __init__(self):

        # TODO: Implement this for task C!
        self.all_solved = False
        self.entrance_exit_paths = dict()

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]):
        """Solver Maze logic:
        Step 1: fetch path from entrance at index 0 to exit index 0
        Steo 2: fetch and find a path from the entrance and exit index 1
        Step 3: return all_solved flag as true if the second path also exits
        """
        # TODO: Implement this for task C!
        self.findPath(maze, entrances, exits, [], 0)
        if self.entrance_exit_paths:
            self.all_solved = self.findPath(maze, entrances, exits, self.entrance_exit_paths[0], 1)

    def getSolverPath(self) -> dict:
        return self.entrance_exit_paths

    def findPath(self, maze: Maze, entrances: Coordinates, exits: List[Coordinates], exclude_path: List[Coordinates], index: int):
        """This function implements the greedy algorithm dijkshara

        Pseudocode
        ----------
        /*Dijkshara Algorithm to find shorted path from an entrance point to exit point
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
        1. Initialize Priority Queue N = [ENTRANCE[IDNEX]]
        2. Set V = EMPTY_LIST
        3. while N not EMPTY do
        4.      set NODE = N.pop()   > get the shortest path node
        5.      V.PUSH(NODE)         > update visited nodes
        6.      if NODE == EXIT[INDEX] then
        7.          set solved path by traversing V
        8.          return True if PATH_LEVEL > 1
        9.      find nearest non-visited, not to be excluded NEIGHBOUR(s)
        10.     N.push(NEIGHBOUR)
        11. end while
        12. return False

        Datastructures Used:
            - min-heap

        Time complexity:
            E(log V) -> for V - vertices & E - Edges

        """
        node_queue = list()                                   # use heap to implement priority Queue
        heapq.heapify(node_queue)
        heapq.heappush(node_queue, Node(entrances[index], 0)) # initialize heap with first node as entrance at index

        visited = dict()
        while node_queue:
            nearest =  heapq.heappop(node_queue)              # fetch the node with shortest distance
            visited.update({nearest.node : nearest})         # Add this nearest node to visited list

            if nearest.node == exits[index]:                 # check if this is the exit
                path = nearest.node                          # set path to node
                m_solverPath = list()                        # initialize sovler path
                path_index = 0
                while path:                                  # loop until no path node found
                    m_solverPath.append(path)                # append current valid path to solved path list
                    path = visited[path].parent              # point "path" to current node's parent
                    path_index += 1                          # increment the path counter

                m_solverPath.reverse()                                   # reverse the list as we added the path frome exit to entrance
                self.entrance_exit_paths.update({index: m_solverPath})   # set the path in entrance_exit_path varaibale
                return path_index > 1                                    # return True if the path length is greater than 1


            neighbours = maze.neighbours(nearest.node)

            # Find neighbours that are not visited in this exploration
            # and is not there in the previous chosen path
            nonVisitedNeighs = [neigh for neigh in neighbours if not maze.hasWall(nearest.node, neigh) and neigh not in exclude_path]

            for neigh in nonVisitedNeighs:
                neigh_distance = nearest.distance + manhattanHeuristics(neigh, nearest.node) # get manhattan distance from selected to neighbour

                if (neigh not in visited or neigh_distance < visited[neigh].distance):       # the new neighbor was not visited or has a new shorted distance
                    heapq.heappush(node_queue, Node(neigh, neigh_distance, nearest.node))     # add the new neighbor to heap with new parent and distance

        return False
