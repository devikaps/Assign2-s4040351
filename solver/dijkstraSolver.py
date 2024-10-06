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
        Process each nodes from frontier (Step 4, 5)
        Return once the exit is found (Step 6)
        Explore the child nodes until exit is found (Step 7-8)

    Pseudocode
    -----------
        Step 1: solver_path <- Node(vertices)
        Step 2: frontier <- priority queue
        Step 3: visited <- visited nodes

        Step 4: while NOT_EMPTY(frontier) do
        Step 5:     node <- POP(frontier)

        Step 6:     if exist found: then populate the path and return result

        Step 7:     for each child in Expand(node) do
        Step 8:         child <- child_node
        Step 9:         if child not in visited and child.path_cost < old_path_cost:
        Step 10:         set visited[s].path_cost = child.path_cost
        Step 11:         add child to frontier and update with new parent if exists


    """
    def __init__(self):
        # TODO: Implement this for task A!
        self.m_cellsExplored = 0
        self.m_entranceUsed = None
        self.m_exitUsed = None
        self.m_solverPath: List[Coordinates] = list()

    def manhattanHeuristics(self, xy1:Coordinates, xy2:Coordinates):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs(xy1.getRow() - xy2.getRow()) + abs(xy1.getCol() - xy2.getCol())

    class Node:
        """Node Object defining a node with its distance from starting point"""
        def __init__(self, node, distance, parent=None):
            self.node = node
            self.distance = distance
            self.parent = parent

        def __lt__(self, node):
            return self.distance < node.distance


    def solveMaze(self, maze: Maze, entrance: Coordinates):
        """Implementing Dijakshara Algorithm"""
        # TODO: Implement this for task A!

        frontier = list()
        heapq.heapify(frontier)
        heapq.heappush(frontier, self.Node(entrance, 0))

        visited = dict()
        while frontier: # Step 4
            # Pop the next nearest node (node with shortest distance) and update visited list
            nearest =  heapq.heappop(frontier)
            visited.update({nearest.node : nearest})
            self.m_cellsExplored += 1

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

            # Explore the neighbors
            neighbours = maze.neighbours(nearest.node)

            nonVisitedNeighs = [neigh for neigh in neighbours if not maze.hasWall(nearest.node, neigh)]

            for neigh in nonVisitedNeighs:
                neigh_distance = nearest.distance + self.manhattanHeuristics(neigh, nearest.node)

                if (neigh not in visited or neigh_distance < visited[neigh].distance):
                    heapq.heappush(frontier, self.Node(neigh, neigh_distance, nearest.node))
                    if neigh in visited:
                        visited[neigh] = self.Node(neigh, neigh_distance,nearest.node)
