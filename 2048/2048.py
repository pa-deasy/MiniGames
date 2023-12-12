from enum import IntEnum
import random
from typing import List


class Direction(IntEnum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT  = 4


class Position:
    row: int
    column: int
    
    def left(self):
        return Position(self.row, self.column - 1) if self.column - 1 >= 0 else None


class Tile:
    value: int


class Board:
    size = 4
    score: int
    is_playable: bool
    layout = List[List[Tile]]
    
    def __init__(self):
        self.score = 0
        self.is_playable = True
        columns = [None] * self.size
        self.layout = columns * self.size
        
        self.generate_tile()
        self.generate_tile()
        
        
    def generate_tile(self):
        possible_tile_values = [2, 4]
        empty_positions = []
        for row_index in range(self.size):
            for column_index in range(self.size):
                if self.layout[row_index][column_index] is None:
                    empty_positions.append(Position(row_index, column_index))
        
        if not empty_positions:
            self.is_playable = False
            return

        random_position = random.choice(empty_positions)
        random_value = random.choice(possible_tile_values)
        self.layout[random_position.row][random_position.column] = random_value
        
        
    def play_move(self, direction: Direction):
        rotations_to_left = Direction.LEFT - direction
        rotations_back = Direction
        
        self.rotate_n_times(rotations_to_left)
        
        self.play_move_left()
        
        self.rotate_n_times(rotations_back)
        
        
    def play_move_left(self):
        for row_index in range(self.size):
            last_free_space = None
            for column_index in range(self.size):
                position = Position(row_index, column_index)
                
                last_free_space = self.try_move(last_free_space, position)
                last_free_space = self.try_merge(last_free_space, position)
           
                
    def try_move(self, last_free_space: int, position: Position):
        if self.layout[position.row][position.column] is None:
            return last_free_space if last_free_space else position.column
        
        if last_free_space is None:
            return last_free_space
        
        self.layout[position.row][last_free_space] = self.layout[position.row][position.column]
        self.layout[position.row][position.column] = None
        return last_free_space + 1
        

    def try_merge(self, last_free_space: int, position: Position):
        position = Position(position.row, last_free_space - 1) if last_free_space else position
        
        left_position = position.left()
        if not left_position:
            return last_free_space
        
        if self.layout[left_position.row][left_position.column].value == self.layout[position.row][position.column].value:
            self.layout[left_position.row][left_position.column].value *= 2
            self.score += self.layout[left_position.row][left_position.column].value
            self.layout[position.row][position.column]
            return last_free_space - 1
        
        return last_free_space
    
        
    def rotate_n_times(self, rotations: int):
        for n in range(rotations):
            self.rotate()
        
    
    def rotate(self):
        max_layer = round(self.size/2)

        for layer in range(0, max_layer):
            first = layer
            last = self.size - 1 - layer
            for index in range(first, last):
                offset = index - layer
                
                top = self.layout[first][index]
                self.layout[first][index] = self.layout[last - offset][first]
                self.layout[last - offset][first] = self.layout[last][last - offset]
                self.layout[last][last - offset] = self.layout[index][last]
                self.layout[index][last] = top


class Game:
    def start(self):
        board = Board()
        
        while board.is_playable and not self.is_won(board.score):
            direction = self.get_player_move()
            
            board.play_move(direction)
        
        
    def get_player_move(self):
        # do something to get move
        return
        
        
    def is_won(self, score: int):
        return score == 2048