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
    def __init__(self, node, distance, heuristic, path=[]):
        self.node = node            # co-ordinates of the node
        self.distance = distance    # total distance to this node
        self.heuristic= heuristic   # total distance to this node
        self.path = path            # path to this node

    def __lt__(self, node):         # overwriting the less-than method for this class
        return self.heuristic < node.heuristic


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
            path_cost = list()
            for index in range(0, len(entrances)):
                path_found = self.findPath(maze, entrances[index], exits[index], exclude_paths)
                if path_found:
                    self.entrance_exit_paths.update({index: path_found[0]})
                    exclude_paths.extend(path_found[0])
                    path_cost.append(path_found[1])

            self.all_solved = (len(self.entrance_exit_paths) == len(entrances))
            if self.all_solved:
                for index in range(0, len(entrances)):
                    print(f"Entrance-Exit-Pair: {index+1}\t Path Cost:{path_cost[index]}")
        except Exception as e:
            print("Invalid Input Configuration. No paths generated!", str(e))

    def getSolverPath(self) -> dict:
        return self.entrance_exit_paths

    def findPath(self, maze: Maze, entrance: Coordinates, exit: Coordinates, exclude_path: List[Coordinates]):
        """This function implements the greedy algorithm Dijkstra

        Pseudocode
        ----------
        /*Dijkstra Algorithm to find shorted path from an entrance point to exit point
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
        1. Initialize Priority Queue N = (ENTRANCES, 0, [ENTRANCE])
        2. Set V = EMPTY_LIST
        3. while N not EMPTY do
        4.      set NODE = N.pop()   > get the shortest path node
        5.      V.PUSH(NODE)         > update visited nodes
        6.      if NODE == EXIT then return NODE.path
        7.      find selected non-visited, not to be excluded NEIGHBOUR(s)
        8.        distance = NEIGHBOUR.distance + HEURISTICS(NEIGHBOUR, EXIT)
        9.        if not visited(NEIGHBOUR) or visited.distance > distance
        10.          N.push(NEIGHBOUR, distance, PATH(NEIGHBOUR))
        11. end while
        12. return EMPTY_LIST

        Datastructures Used:
            - min-heap

        Time complexity:
            The worst case scenario where there are no paths
            O(n) = E(log V) => V:vertices, E:Edges

        """
        node_queue = list()                                   # use heap to implement priority Queue
        heapq.heapify(node_queue)
        heapq.heappush(node_queue, Node(entrance, 0, 0, [entrance])) # initialize heap with first node as entrance at index
        visited = dict()

        while node_queue:
            selected =  heapq.heappop(node_queue)             # fetch the node with shortest distance
            visited.update({selected.node : selected})        # Add this selected node to visited list

            if selected.node == exit:                         # check if this is the exit
                return (selected.path, selected.distance)     # return True if the path length is greater than 1

            nonVisitedNeighs = [(neigh, getCellWeight(neigh, selected.node, maze)) for neigh in maze.neighbours(selected.node) if not maze.hasWall(selected.node, neigh) and neigh not in exclude_path]

            for neigh, distance in nonVisitedNeighs:
                neigh_distance = distance + selected.distance
                neigh_heuristic = self.manhattanHeuristics(exit, selected.node)          # get manhattan distance from selected to exit

                if (neigh not in visited or neigh_heuristic < visited[neigh].heuristic): # the new neighbor was not visited or has a new shorted distance
                    neigh_path = [neigh]
                    neigh_path.extend(selected.path)                                     # find the path towards this neighbour
                    heapq.heappush(node_queue, Node(neigh, neigh_distance, neigh_heuristic, neigh_path)) # add the new neighbor to heap with new parent and distance

        return []

    def manhattanHeuristics(self, xy1:Coordinates, xy2:Coordinates):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs(xy1.getRow() - xy2.getRow()) + abs(xy1.getCol() - xy2.getCol())


# Added since the file based maze creations was not returning the proper distance
# since the vertices were not proper while taking weightage
def getCoordinate(vert: Coordinates, maze: Maze):
   vertices = maze.getVetrices()
   for vertex in vertices:
      if vertex == vert:
         return vertex

def getCellWeight(vert1: Coordinates, vert2: Coordinates, maze: Maze):
   return maze.edgeWeight(getCoordinate(vert1,maze), getCoordinate(vert2,maze))