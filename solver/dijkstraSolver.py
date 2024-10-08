# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Dijkstra's maze solver.
#
# __author__ =  Devika Sheeja
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.util import Coordinates
from maze.maze import Maze
from student.lib import Node
from student.lib import manhattanHeuristics
import heapq

class DijkstraSolver():
    """
    Dijakshara
    -----------
    Dijakshara works by exploring the shortest nearest neighbour
    It makes use of a heuristic for finiding the best distance
    Here, manhattan distance is used as the heuristics.
    Priority queue (min) is implemented using heapq

    Logic in Short
    -------------------------
        Start processing from entrance node (Step 1 to 3)
        Process each nodes from node_queue (Step 4, 5)
        Return once the exit is found (Step 6)
        Explore the child nodes until exit is found (Step 7-8)

    Pseudocode
    -----------
        Step 1: solver_path <- Node(vertices)
        Step 2: node_queue <- priority queue
        Step 3: visited <- visited nodes
        Step 4: while NOT_EMPTY(node_queue) do
        Step 5:     node <- POP(node_queue)
        Step 6:     if exist found: then populate the path and return result
        Step 7:     for each child in Expand(node) do
        Step 8:         child <- child_node
        Step 9:         if child not in visited and child.path_cost < old_path_cost:
        Step 10:         set visited[s].path_cost = child.path_cost
        Step 11:         add child to node_queue for re-processing

    Datastructures Used:
        - min-heap

    Time complexity:
        E(log V) -> for V - vertices & E - Edges

    """
    def __init__(self):
        # TODO: Implement this for task A!
        self.m_cellsExplored = 0
        self.m_entranceUsed = None
        self.m_exitUsed = None
        self.m_solverPath: List[Coordinates] = list()

    def solveMaze(self, maze: Maze, entrance: Coordinates):
        """Implementing Dijakshara Algorithm"""
        # TODO: Implement this for task A!

        node_queue = list()
        heapq.heapify(node_queue)                                 # use Heap to implement Priority Queue
        heapq.heappush(node_queue, Node(entrance, 0))             # push Entrance to the the queue

        visited = dict()                                          # set visited nodes as Empty
        while node_queue:                                         # Step 4
            nearest =  heapq.heappop(node_queue)                  # Pop the next nearest node (node with shortest distance) and update visited list
            visited.update({nearest.node : nearest})              # add the processing node to visited list

            # When the current processing node is the exit
            # Update solver path and reutn
            if nearest.node in maze.getExits():
                path = nearest.node
                while path:
                    self.m_solverPath.append(path)
                    path = visited[path].parent

                self.m_solverPath.reverse()
                self.m_entranceUsed = entrance
                self.m_exitUsed = nearest.node
                return

            self.m_cellsExplored += 1                             # increment explored nodes count
            neighbours = maze.neighbours(nearest.node)            # Explore the neighbors
            nonVisitedNeighs = [neigh for neigh in neighbours if not maze.hasWall(nearest.node, neigh)]

            for neigh in nonVisitedNeighs:                                                      # process all edges that are not walls
                neigh_distance = nearest.distance + manhattanHeuristics(neigh, nearest.node)    # (ditance to neighbor + the parents distance from starting node)
                if (neigh not in visited or neigh_distance < visited[neigh].distance):          # If not visited or with a new shorted distance
                    heapq.heappush(node_queue, Node(neigh, neigh_distance, nearest.node))       # add it to queue for (re-)processng
