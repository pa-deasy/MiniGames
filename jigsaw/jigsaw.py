from dataclasses import dataclass
from enum import Enum, IntEnum
from math import sqrt
from typing import Dict, List

from linked_list import LinkedList


class Orientation(IntEnum):
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4
    
    def get_opposite(self) -> 'Orientation':
        if self == Orientation.LEFT:
            return Orientation.RIGHT
        elif self == Orientation.RIGHT:
            return Orientation.LEFT
        elif self == Orientation.TOP:
            return Orientation.BOTTOM
        elif self == Orientation.BOTTOM:
            return Orientation.TOP
        else:
            return None


class Shape(Enum):
    OUTER = 'outer'
    INNER = 'inner'
    FLAT = 'flat'
    
    def get_opposite(self) -> 'Shape':
        if self == Shape.OUTER:
            return Shape.INNER
        elif self == Shape.INNER:
            return Shape.OUTER
        else:
            None
            

@dataclass
class Edge:
    id: int
    shape: Shape
    parent_piece: 'Piece'
    
    def fits_with(self, other: 'Edge') -> bool:
        return False
    

class Piece:
    edges: Dict[Orientation, Edge]
    
    def rotate_edges(self, rotations: int) -> None:
        while rotations > 0:
            left = self.edges[Orientation.LEFT]
            self.edges[Orientation.LEFT] = self.edges[Orientation.BOTTOM]
            self.edges[Orientation.BOTTOM] = self.edges[Orientation.RIGHT]
            self.edges[Orientation.RIGHT] = self.edges[Orientation.TOP]
            self.edges[Orientation.TOP] = left
    
    def set_edge_as_orientation(self, edge: Edge, orientation: Orientation) -> None:
        current_orientation = [o for (o, e) in self.edges.items() if e == edge]
        rotation_diff = orientation - current_orientation if orientation >= current_orientation else orientation + 4 - current_orientation
        
        self.rotate_edges(rotation_diff)
        

class Puzzle:
    pieces: LinkedList[Piece]
    matching_edges: Dict[int, int]
    solution: List[List[Piece]]
    size: int
    
    def __init__(self, pieces: List[Piece], matching_edges: Dict[int, int], size: int) -> None:
        self.pieces = pieces
        self.matching_edges = matching_edges
        row = [None] * size
        rows = row * size
        self.solution = rows
        self.size = sqrt(len(pieces))
        
    def solve(self) -> List[List[Piece]]:
        corner_pieces = LinkedList()
        border_pieces = LinkedList()
        inside_pieces = LinkedList()
        self._group_pieces(corner_pieces, border_pieces, inside_pieces)
        
        for row in range(self.size):
            for column in range(self.size):
                pieces_to_search = self._get_pieces_to_search(corner_pieces, border_pieces, inside_pieces)
                self._fit_next_edge(pieces_to_search, row, column)

        return self.solution
    
    def _group_pieces(self, corner_pieces: LinkedList, border_pieces: LinkedList, inside_pieces: LinkedList) -> None:
            for piece in self.pieces:
                flat_edges_count = len([e.shape for e in piece.edges if e.shape == Shape.FLAT])
                
                if flat_edges_count == 2:
                    corner_pieces.add(piece)
                elif flat_edges_count == 1:
                    border_pieces.add(piece)
                else: 
                    inside_pieces.add(piece)
    
    def _get_pieces_to_search(self, corner_pieces: LinkedList, border_pieces: LinkedList, inside_pieces: LinkedList, row: int, column: int) -> LinkedList:
        if (row == 0 and (column == 0 or column == self.size - 1)) or (row == self.size - 1 and (column == 0 or column == self.size - 1)):
            return corner_pieces
        elif row == 0 or row == self.size - 1 or column == 0 or column == self.size - 1:
            return border_pieces
        else:
            return inside_pieces
        
    def _fit_next_edge(self, pieces_to_search: LinkedList, row: int, column: int) -> None:
        if row == 0 and column == 0:
            p: Piece = pieces_to_search.remove_first().value
            self._orient_top_left_corner(p)
            self.solution[0][0] = p     
        else:
            piece_to_match = self.solution[row - 1][0] if column == 0 else self.solution[row][column - 1]
            orientation_to_match = Orientation.BOTTOM if column == 0 else Orientation.BOTTOM
            edge_to_match = piece_to_match.edges.get(orientation_to_match)
            
            edge = self._get_matching_edge(edge_to_match, pieces_to_search)
            if edge == None:
                raise Exception("Can't solve")
            
            orientation = orientation_to_match.get_opposite()
            self._set_edge_in_solution(pieces_to_search, edge, row, column, orientation)
            
    def _orient_top_left_corner(self, piece: Piece) -> None:
        # find 2 flad edges and place them to match the outside of puzzle
        return
    
    def _get_matching_edge(self, edge_to_match: Edge, pieces_to_search: LinkedList) -> Edge:
        matching_id = self.matching_edges.get(edge_to_match.id)
        for p in pieces_to_search:
            for edge in p.edges:
                if edge.id == matching_id:
                    return edge
        return None
        
    def _set_edge_in_solution(self, pieces: LinkedList, edge: Edge, row: int, column: int, orientation: Orientation) -> None:
        piece = edge.parent_piece
        piece.set_edge_as_orientation(edge, orientation)
        pieces.delete_node(piece)
        self.solution[row][column] = piece
        
    
        
    
            
    
    