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
import heapq


class Node:
    """Node Object defining a node with its distance from starting point"""
    def __init__(self, node, distance, parent=None, path=[]):
        self.node = node
        self.distance = distance
        self.parent = parent
        self.path = path

    def __lt__(self, node):
        return self.distance < node.distance


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
        try:
            exclude_paths = list()
            for index in range(0, len(entrances)):
                path_found = self.findPath(maze, entrances[index], exits[index], exclude_paths)
                if path_found:
                    self.entrance_exit_paths.update({index: path_found})
                    exclude_paths.extend(path_found)

            self.all_solved = (len(self.entrance_exit_paths) == len(entrances))
        except ValueError:
            print("Invalid Input Configuration. No paths generated!")

    def getSolverPath(self) -> dict:
        return self.entrance_exit_paths

    def findPath(self, maze: Maze, entrance: Coordinates, exit: Coordinates, exclude_path: List[Coordinates]):
        """This function implements the greedy algorithm dijkshara

        Pseudocode
        ----------
        /*Dijkshara Algorithm to find shorted path from an entrance point to exit point
          Input:
                maze - Class that provides the maze related details, including edge, edge-weight, walls, etc
                entrances - an array where the entrances are provided
                exits - an array where the exits are provided
                exclude_path - Nodes to be excluded when finding the path
                entrance_index - index of the entrance and exit for which the path to be found
          Output:
                Returns True if a path is found else False
                Also, ammends the path in the dictionary at the index of self.entrance_exit_paths
        */

        Steps:
        ------
        1. Initialize Priority Queue N = [ENTRANCES[ENTRANCE_INDEX]]
        2. Set V = EMPTY_LIST
        3. while N not EMPTY do
        4.      set NODE = N.pop()   > get the shortest path node
        5.      V.PUSH(NODE)         > update visited nodes
        6.      if NODE == EXIT[INDEX] then
        7.          set solved path by traversing V
        8.          return SOLVED_PATH
        9.      find nearest non-visited, not to be excluded NEIGHBOUR(s)
        10.     N.push(NEIGHBOUR)
        11. end while
        12. return EMPTY_LIST

        Datastructures Used:
            - min-heap

        Time complexity:
            E(log V) -> for V - vertices & E - Edges

        """
        node_queue = list()                                   # use heap to implement priority Queue
        heapq.heapify(node_queue)
        heapq.heappush(node_queue, Node(entrance, 0)) # initialize heap with first node as entrance at index

        visited = dict()
        while node_queue:
            nearest =  heapq.heappop(node_queue)             # fetch the node with shortest distance
            visited.update({nearest.node : nearest})         # Add this nearest node to visited list

            if nearest.node == exit:                         # check if this is the exit
                path = nearest.node                          # set path to node
                m_solverPath = list()                        # initialize sovler path
                while path:                                  # loop until no path node found
                    m_solverPath.append(path)                # append current valid path to solved path list
                    path = visited[path].parent              # point "path" to current node's parent
                m_solverPath.reverse()                       # reverse the list as we added the path frome exit to entrance
                return m_solverPath                          # return True if the path length is greater than 1


            neighbours = maze.neighbours(nearest.node)       # Find non visited and non overlapping neighbours
            nonVisitedNeighs = [neigh for neigh in neighbours if not maze.hasWall(nearest.node, neigh) and neigh not in exclude_path]

            for neigh in nonVisitedNeighs:
                neigh_distance = nearest.distance + self.manhattanHeuristics(exit, nearest.node) # get manhattan distance from selected to exit

                if (neigh not in visited or neigh_distance < visited[neigh].distance):       # the new neighbor was not visited or has a new shorted distance
                    heapq.heappush(node_queue, Node(neigh, neigh_distance, nearest.node))    # add the new neighbor to heap with new parent and distance

        return []

    def manhattanHeuristics(self, xy1:Coordinates, xy2:Coordinates):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs(xy1.getRow() - xy2.getRow()) + abs(xy1.getCol() - xy2.getCol())

