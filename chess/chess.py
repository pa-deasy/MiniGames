from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class Color(Enum):
    BLACK = 'Black'
    WHITE = 'White'
    
    def get_opposite(self) -> 'Color':
        return Color.WHITE if self == Color.BLACK else Color.WHITE


@dataclass
class Position:
    row: int
    column: int
    
    
@dataclass
class Move:
    initial: Position
    target: Position
    turn: Color
    

class Piece():
    position: Position
    color: Color
    
    def __init__(self, position: Position, color: Color) -> None:
        self.position = position
        self.color = color
    
    def can_move_to(self, target: Position, board: List[List['Piece']]) -> bool:
        ...
        
        
class Pawn(Piece):
    def can_move_to(self, target: Position, layout: List[List['Piece']]) -> bool:
        row_diff = target.row - self.position.row
        abs_column_diff = abs(target.column - self.position.column)
        target_piece = layout[target.row][target.column]
        
        expected_direction = 1 if self.color == Color.BLACK else -1
        if row_diff != expected_direction:
            return False
        
        return (not target_piece and self.position.column == target.column) or (target_piece and abs_column_diff == 1)
    

class King(Piece):
    def can_move_to(self, target: Position, layout: List[List['Piece']]) -> bool:
        abs_row_diff = abs(target.row - self.position.row)
        abs_column_diff = abs(target.column - self.position.column)
        return abs_row_diff <= 1 and abs_column_diff <= 1
    

class Queen(Piece):
    def can_move_to(self, target: Position, layout: List[List['Piece']]) -> bool:
        return Castle(self.position, self.color).can_move_to(target, layout) or Bishop(self.position, self.color).can_move_to(target, layout)
    

class Knight(Piece):
    def can_move_to(self, target: Position, layout: List[List['Piece']]) -> bool:
        abs_row_diff = abs(target.row - self.position.row)
        abs_column_diff = abs(target.column - self.position.column)
        
        return (abs_row_diff == 1 and abs_column_diff == 2) or (abs_row_diff == 2 and abs_column_diff == 1)
        
    
class Castle(Piece):
    def can_move_to(self, target: Position, layout: List[List['Piece']]) -> bool:
        row_diff = target.row - self.position.row
        column_diff = target.column - self.position.column
        can_move_in_direction = row_diff == 0 or column_diff == 0
        
        if not can_move_in_direction:
            return False
        
        if row_diff == 0:
            lower, higher = self.position.column, target.column if self.position.column < target.column else target.column, self.position.column
            for column in range(lower, higher):
                if layout[target.row][column] is not None:
                    return False
        elif column_diff == 0:
            lower, higher = self.position.row, target.row if self.position.row < target.row else target.row, self.position.row
            for row in range(lower, higher):
                if layout[row][target.column] is not None:
                    return False  
                
        return True
        

class Bishop(Piece):
    def can_move_to(self, target: Position, layout: List[List['Piece']]) -> bool:
        row_diff = target.row - self.position.row
        column_diff = target.column - self.position.column
        can_move_in_direction = abs(row_diff) == abs(column_diff)
        
        if not can_move_in_direction:
            return False

        top_left_to_bottom_right = (row_diff > 0 and column_diff > 0) or (row_diff < 0 and column_diff < 0)
        
        lower_row, higher_row = self.position.row, target.row if self.position.row < target.row else target.row, self.position.row
        lower_column = self.position.column if self.position.column < target.column else target.column
        
        if top_left_to_bottom_right:
            for row in range(lower_row, higher_row):
                if layout[row][lower_column] is not None:
                        return False
                lower_column += 1
        else:
            for row in range(higher_row, lower_row, -1):
                if layout[row][lower_column] is not None:
                        return False
                lower_column += 1
                
        return True
        
    
class Board:
    size: int = 8
    layout: List[List[Piece]]
    is_checkmate: bool
    captured_pieces: Dict[Color, List[Piece]]
    
    def __init__(self) -> None:
        row = [None] * self.size
        self.layout = row * self.size
        self.set_up_pawns()
        self.set_up_back_rows()
        self.is_checkmate = False
        self.captured_pieces = {}
        self.captured_pieces[Color.WHITE] = []
        self.captured_pieces[Color.BLACK] = []
    
    def set_up_pawns(self):
        for column in range(self.size):
            self.layout[1][column] = Pawn(Position(row=1, column=column), Color.BLACK)
            self.layout[6][column] = Pawn(Position(row=6, column=column), Color.WHITE)
            
    def set_up_back_rows(self):
        for column in range(self.size):
            if column == 0 or column == 7:
                self.layout[0][column] = Castle(Position(row=0, column=column), Color.BLACK)
                self.layout[7][column] = Castle(Position(row=7, column=column), Color.WHITE)
            elif column == 1 or column == 6:
                self.layout[0][column] = Knight(Position(row=0, column=column), Color.BLACK)
                self.layout[7][column] = Knight(Position(row=7, column=column), Color.WHITE)
            elif column == 2 or column == 5:
                self.layout[0][column] = Bishop(Position(row=0, column=column), Color.BLACK)
                self.layout[7][column] = Bishop(Position(row=7, column=column), Color.WHITE)
            elif column == 3:
                self.layout[0][column] = Queen(Position(row=0, column=column), Color.BLACK)
                self.layout[7][column] = Queen(Position(row=7, column=column), Color.WHITE)
            elif column == 4:
                self.layout[0][column] = King(Position(row=0, column=column), Color.BLACK)
                self.layout[7][column] = King(Position(row=7, column=column), Color.WHITE)
                
    def is_valid_move(self, move: Move) -> bool:
        if not self.is_within_board(move.target):
            return False
        
        piece = self.layout[move.initial.row][move.initial.column]
        if not piece:
            return False
        
        correct_turn = piece.color == move.turn
        not_occupied = self.target_not_occupied_by_same_color(move.turn, move.target)
        can_move_to = piece.can_move_to(move.target, self.size)
        
        return correct_turn and not_occupied and can_move_to
    
    def is_within_board(self, target: Position) -> bool:
        return target.row >= 0 and target.row < self.size and target.column >= 0 and target.column < self.size
    
    def target_not_occupied_by_same_color(self, turn: Color, target: Position) -> bool:
        target_piece = self.layout[target.row][target.column]
        return target_piece is None or target_piece.color == turn.get_opposite()
    
    def play_move(self, move: Move) -> None:
        piece = self.layout[move.initial.row][move.initial.column]
        target = self.layout[move.target.row][move.target.column]
        
        if type(target) == King:
            self.is_checkmate = True
        
        piece.position.row = target.position.row
        piece.position.column = target.position.column
        self.layout[move.target.row][move.target.column] = piece
        self.layout[move.initial.row][move.initial.column] = None
        
        if target:
            self.captured_pieces[target.color].append(target)

           
class Game:
    def play(self):
        board = Board()
        turn = Color.WHITE
        
        while not board.is_checkmate:
            move = self.get_player_move()
            
            is_valid = board.is_valid_move(move)
            
            if is_valid:
                board.play_move(move)
                turn = turn.get_opposite()
            else:
                print('Not a valid move, try again')
            
    def get_player_move(self) -> Move:
        return Move()