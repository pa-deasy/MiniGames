from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PlayerMarker(Enum):
    X = 0
    O = 1
    

@dataclass
class MarkerPosition:
    row_position: int
    column_position: int
    
    def is_outside_of_board(self) -> bool:
        return self._is_outside(self.row_position) or self._is_outside(self.column_position)
    
    def _is_outside(self, position: int) -> bool:
        return position > Board.BOARD_SIZE or position <= Board.BOARD_AXIS_POINT
    
    
class Board:
    BOARD_AXIS_POINT: int = 0
    BOARD_SIZE: int = 3

    value: list[list[Optional[PlayerMarker]]]
    
    def __init__(self):
        self.value = self._setup()
        
    def _setup(self) -> list[list[Optional[PlayerMarker]]]:
        board = []
        
        for row_index in range(self.BOARD_AXIS_POINT, self.BOARD_SIZE):
            row = []
            for column_index in range(self.BOARD_AXIS_POINT, self.BOARD_SIZE):
                row.append(None)
                
            board.append(row)
            
        return board
    
    def get_player_marker(self, position: MarkerPosition) -> PlayerMarker:
        return self.value[position.row_position - 1][position.column_position - 1]
    
    def set_player_marker(self, position: MarkerPosition, player_marker: PlayerMarker) -> None:
        self.value[position.row_position - 1][position.column_position - 1] = player_marker
        
    def has_winning_line(self) -> bool:
        return self._has_horizontal_win() or self._has_vertical_win() or self._has_diagonal_win()
    
    def _has_vertical_win(self) -> bool:
        for column_index in range(Board.BOARD_AXIS_POINT, self.BOARD_SIZE):
            first_marker = self.get_player_marker(MarkerPosition(row_position=self.BOARD_AXIS_POINT, column_position=column_index))
            if first_marker == None:
                continue
            match = True
            for row_index in range(Board.BOARD_AXIS_POINT + 1, self.BOARD_SIZE):
                next_marker = self.get_player_marker(MarkerPosition(row_position=row_index, column_position=column_index))
                if next_marker != first_marker:
                    match = False
                
            if match == True:
                return True
        
        return False
    
    def _has_horizontal_win(self) -> bool:
        for row_index in range(Board.BOARD_AXIS_POINT, self.BOARD_SIZE):
            first_marker = self.get_player_marker(MarkerPosition(row_position=row_index, column_position=self.BOARD_AXIS_POINT))
            if first_marker == None:
                continue
            match = True
            for column_index in range(Board.BOARD_AXIS_POINT + 1, self.BOARD_SIZE):
                next_marker = self.get_player_marker(MarkerPosition(row_position=row_index, column_position=column_index))
                if next_marker != first_marker:
                    match = False
                
            if match == True:
                return True
        
        return False
    
    def _has_diagonal_win(self) -> bool:
        return self._has_left_diagonal_win() or self._has_right_diagonal_win()
    
    def _has_left_diagonal_win(self) -> bool:
        first_marker = self.get_player_marker(MarkerPosition(row_position=self.BOARD_AXIS_POINT, column_position=self.BOARD_AXIS_POINT))
        if first_marker == None:
            return False
        match = True
        for index in range(Board.BOARD_AXIS_POINT + 1, self.BOARD_SIZE):
            next_marker = self.get_player_marker(MarkerPosition(row_position=index, column_position=index))
            if next_marker != first_marker:
                match = False
                
        if match == True:
            return True
        
        return False
    
    def _has_right_diagonal_win(self) -> bool:
        row_index = self.BOARD_AXIS_POINT + 1
        column_index = self.BOARD_SIZE
        first_marker = self.get_player_marker(MarkerPosition(row_position=row_index, column_position=column_index))
        if first_marker == None:
            return False
        match = True
        while row_index < self.BOARD_SIZE:
            row_index += 1
            column_index -= 1
            next_marker = self.get_player_marker(MarkerPosition(row_position=row_index, column_position=column_index))
            if next_marker != first_marker:
                match = False
                
        if match == True:
            return True
        
        return False


class GameState:
    player_turn: PlayerMarker
    is_won: bool
    board: Board
    
    def __init__(self):
        self.player_turn = PlayerMarker.X
        self.is_won = False
        self.board = Board()
