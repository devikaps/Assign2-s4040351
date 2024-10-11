"""This is a common library created for the re-use of common classes
    As Confirmed with Ms. Elham.

    Components in this package includes:
        - is_bounday(function):      to check if the cell is a boundary
        - get_walls(function):       returns walls that are not boundaries for a maze
        - UnionFind(Class):          Union-Find datastructure(disjoint) implementation

"""


from maze.maze import Maze
from maze.util import Coordinates

class UnionFind():
    """Disjoint set class to be used for implemeting union-find datastructure

    Psuedocode:
        Step 1: Intiialize the datastructure
                - set vertices as their parent itself

        Step 2: Find operation definition
                - find the root of the node (initially it will be the node itself)

        Step 3: Union operation
                - If the parents for both vertices are different then its a disjoint set
                - Merge the disjoint sets by setting the parent as same for both
                - Returns True for disjoint set, else return False
    """
    def __init__(self, vertices: Coordinates) -> None:
        """Step 1:"""
        self.parent = dict()
        for vertex in vertices:                 # set all vertices as its own parent
            self.parent.update({vertex: vertex})


    def find(self, vertex):
        """Step #2."""
        if self.parent[vertex] != vertex:
            return self.find(self.parent[vertex])
        return vertex                           # if parent is the vertex (inital case)

    def union(self, vertex1, vertex2):
        """Step #3."""
        parent1 = self.find(vertex1)
        parent2 = self.find(vertex2)

        if parent1 == parent2: return False     # not a disjoint set and will not merge two sections

        self.parent[parent1] = parent2          # Setting the new parent, disjoint sets and merges two sections
        return True


def is_boundary(cell:Coordinates, maze:Maze):
    """Function to check if a cell is in the boundary"""
    if (cell.getRow() >= 0 and cell.getRow() < maze.rowNum() and cell.getCol() >= 0 and cell.getCol() < maze.colNum()):
        return False # not a boundary
    return True # a boundary



def get_walls(maze: Maze) ->list():
    """Building heap with edges and their weights"""
    edges = list()
    for edge in maze.getEdges():                    # parse all edges and fetch all that has wall and not a boundary
        if edge[2] and not is_boundary(edge[0], maze) and not is_boundary(edge[1], maze):
            edges.append((edge, maze.edgeWeight(edge[0],edge[1]))) # tuple: (edge, edge.weight)

    edges = sorted(edges, key = lambda x:x[1])      # sort edges using weight the second index value in the tuple
    return edges
