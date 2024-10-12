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
from math import inf
import heapq


class Node:
    """Node Object defining a node with its distance from starting point"""
    def __init__(self, node, path_to_node, distance_to_node=0):
        self.node = node                    # co-ordinates of the node
        self.path = path_to_node            # path to this node
        self.distance = distance_to_node    # total distance to this node

    def __lt__(self, node):
        return True                         # normal FIFO queue with no priority

class bruteForceSolver():

    def __init__(self):
        # TODO: Implement this for task B!
        self.all_solved = False
        self.entrance_exit_paths = dict()

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]):
        # TODO: Implement this for task B!
        """Solver Maze logic:
        1.	Find all possible paths from an entrance to the corresponding exit
        2.	Find the possibility of a path that does not overlap with the possible paths for another entrance-exit pairs
        3.	The process return boolean TRUE with the shortest non-overlapping if successful
        4.	If not successful, it returns boolean FALSE
        """
        try:
            # Fetch all possible paths
            possible_paths = {}
            for entrance_index in range(0, len(entrances)):
                possible_paths.update({entrance_index: self.findPath(maze, entrances[entrance_index], exits[entrance_index])})

            solved_paths = list()
            for entrance, possible_path in possible_paths.items():              # explore the paths noted for all entrance-exit pairs

                shortest_path = (list(), inf)                                   # (path,distance)
                for path, distance in possible_path:                            # find the shortest path possible that is not overlapping
                    isValid = (len(possible_paths) == 1)                        # exit when only one entrance-exit pair
                    if shortest_path[1] < distance: continue                    # with any paths for other entrance-exit pairs
                    for other_entrance, path_list in possible_paths.items():
                        if other_entrance == entrance:                          # Do not check for the same entrance_exit paths
                            continue
                        for other_path, _ in path_list:
                            if not set(other_path).intersection(path):          # checking if there are commong nodes
                                isValid = True                                  # mark as invalid if there are common nodes found
                                break
                    if isValid:
                        shortest_path = (entrance, path, distance, len(possible_path))
                        break

                if shortest_path: solved_paths.append(shortest_path)        # get the shorted possible non-overlapping path

            if len(solved_paths) == len(entrances):
                for entrance, solved_path, distance, total_paths in solved_paths:
                    print(f"Entrance-Exit-Pair {entrance+1} - Path Cost: {distance}\tTotal Paths: {total_paths}")
                    self.entrance_exit_paths.update({entrance: solved_path})      # Set the final best paths if found and mark as solved
                self.all_solved = True

        except Exception as e:
            print("Invalid input configuration. No paths generated!", str(e))

    def getSolverPath(self) -> dict:
        return self.entrance_exit_paths

    def findPath(self, maze: Maze, entrance: Coordinates, exit: Coordinates):
        """This function implements the Breadth First Search(BFS) is implemented as the Brute Force Algorithm here
          Input:
                maze - Class that provides the maze related details, including edge, edge-weight, walls, etc
                entrance - the entrance co-ordinate
                exit - the exit co-ordinate
          Output: Returns all possible paths

        Steps:
        ------
            1. Initialize the stack with entrance
            2. If the current processing node is exit then track the found possible path
            3. Push all neighbours to stack with the below infomration
                - Cell Coordinates
                - Path to reach this node
                - Distance from entance
            4. Process all the neighbours until the stack is empty
            5. reurn the tracked possible paths

        Time complexity:
        ----------------
            The worst case scenario where there are no paths
            with entrance-exit pairs are placed diagonally
            O(n) = VE => V:vertices, E:Edge
        """
        possible_paths = list()
        node_list = [Node(entrance,[entrance],0)]                        # Node(node, path_to_node, distance_to_node)
        visited = dict()                                                 # empty the visited list
        while node_list:
            selected =  node_list.pop(0)                                 # FIFO order fetch for next node
            visited.update({selected.node : selected})                   # Add the processing node to visited list

            if selected.node == exit:                                    # if the node is the expected exit
                possible_paths.append((selected.path, selected.distance))# append the possible paths to exit node
                continue

            neighbours = maze.neighbours(selected.node)                  # Find neighbours that are NON-VISITED & NOT_A_WALL
            nonVisitedNeighs = [(neigh, getCellWeight(selected.node, neigh, maze)) for neigh in neighbours if not maze.hasWall(selected.node, neigh) and neigh not in visited]

            for neigh, distance in nonVisitedNeighs:                     # push neighbours to queue
                path = [neigh]
                path.extend(selected.path)
                total_distance = selected.distance + distance
                neigh_node = Node(neigh, path, total_distance)
                node_list.append(neigh_node)                             # push the neighbour node for processing

        return possible_paths                                            # return the multiple paths found

# Added since the file based maze creations was not returning the proper distance
# since the vertices were not proper while taking weightage
def getCoordinate(vert: Coordinates, maze: Maze):
   vertices = maze.getVetrices()
   for vertex in vertices:
      if vertex == vert:
         return vertex

def getCellWeight(vert1: Coordinates, vert2: Coordinates, maze: Maze):
   return maze.edgeWeight(getCoordinate(vert1,maze), getCoordinate(vert2,maze))
