# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Dijkstra's maze solver.
#
# __author__ =  Devika Sheeja
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.util import Coordinates
from maze.maze import Maze
import heapq
from math import inf

class Node:
    """Node Object defining a node with its distance from starting point"""
    def __init__(self, node, distance, path=[]):
        self.node = node            # co-ordinates of the node
        self.distance = distance    # total distance to this node
        self.path = path            # path to this node

    def __lt__(self, node):         # overwriting the less-than method for this class
        return self.distance < node.distance


class DijkstraSolver():
    """
    Dijkstra
    -----------
    Dijkstra works by exploring the shortest nearest neighbour
    Priority queue (min-heap) is implemented using heapq

    Logic in Short
    -------------------------
        Initialize queue and visited list (Steps 1, 2)
        Process each nodes from node_queue (Steps 4-10)
        Return path once the exit is found (Step 5)
        Explore the child nodes (Step 6-10)

    Pseudocode
    -----------
        Step 1: node_queue <- Node(vertices,distance,path) priority queue
        Step 2: visited <- visited nodes
        Step 3: while NOT_EMPTY(node_queue) do
        Step 4:     node <- POP(node_queue)
        Step 5:     if exist found: then return node.path
        Step 6:     for each child in Expand(node) do
        Step 7:         child <- child_node
        Step 8:         if child not in visited or child.distance < old_distance
        Step 9:             set visited[s].distance = child.distance
        Step 10:            add child to node_queue for re-processing with new path and distance

    Datastructures Used:
        - min-heap

    Time complexity:
        For a worst case scenario where all edges are walls and no path found
        O(e) = E(log V) => V:vertices & E:Edges
    """
    def __init__(self):
        # TODO: Implement this for task A!
        self.m_cellsExplored = 0
        self.m_entranceUsed = None
        self.m_exitUsed = None
        self.m_solverPath: List[Coordinates] = list()

    def solveMaze(self, maze: Maze, entrance: Coordinates):
        """Implementing Dijkstra Algorithm"""
        # TODO: Implement this for task A!
        try:
            node_queue = list()
            heapq.heapify(node_queue)                                 # use Heap to implement Priority Queue
            heapq.heappush(node_queue, Node(entrance, 0, [entrance])) # push Entrance to the the queue

            for vertex in maze.getVetrices():
                if vertex != entrance:
                    heapq.heappush(node_queue, Node(vertex, inf))     # set the distance as infinity for all nodes except entrance

            visited = dict()                                          # set visited nodes as Empty
            while node_queue:                                         # Step 4
                selected =  heapq.heappop(node_queue)                 # Pop the next nearest node (node with shortest distance) and update visited list
                visited.update({selected.node : selected})            # add the processing node to visited list

                if selected.node in maze.getExits():                  # When the current processing node is the exit
                    self.m_solverPath =  selected.path                # Update solver path and reutn
                    self.m_entranceUsed = entrance
                    self.m_exitUsed = selected.node
                    return

                self.m_cellsExplored += 1                             # increment explored nodes count
                nonVisitedNeighs = [(neigh, self.getCellWeight(neigh, selected.node, maze)) for neigh in maze.neighbours(selected.node) if not maze.hasWall(selected.node, neigh)] # Explore the neighbors

                for neigh, distance in nonVisitedNeighs:                         # process all edges that are not walls
                    neigh_distance = distance + selected.distance                # (ditance to neighbor + the parents distance from starting node)
                    if (neigh not in visited or neigh_distance < visited[neigh].distance):    # If not visited or has a new shorter distance
                        neigh_path = [neigh]
                        neigh_path.extend(selected.path)
                        heapq.heappush(node_queue, Node(neigh, neigh_distance, neigh_path)) # add it to queue for (re-)processng

        except Exception as e:
            print("Invalid Configuration! Exisitng process..........",str(e))


    # Added since the file based maze creations was not returning the proper distance
    # since the vertices were not proper while taking weightage
    def getCoordinate(self, vert: Coordinates, maze: Maze):
        vertices = maze.getVetrices()
        for vertex in vertices:
            if vertex == vert:
                return vertex

    def getCellWeight(self, vert1: Coordinates, vert2: Coordinates, maze: Maze):
        return maze.edgeWeight(self.getCoordinate(vert1,maze), self.getCoordinate(vert2,maze))
