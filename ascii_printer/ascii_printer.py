import enum
from typing import Any, List


class Canvas:
    row_size = 6
    column_size = 10
    layers = List[List[List[str]]]
    
    def __init__(self) -> None:
        self.layers = []
        
        
    def new_layer(self) -> List[List[str]]:
        columns = self.column_size * [None]
        return self.row_size * columns
    
    def coordinate_is_within_bounds(self, row: int, column: int):
        return row < self.row_size and row >= 0 and column < self.column_size and column >= 0

    def DRAW_RECTANGLE(self, fill_character: str, left_x: int, top_y: int, right_x: int, bottom_y:int):
        if not self.coordinate_is_within_bounds(top_y, left_x) or not self.coordinate_is_within_bounds(bottom_y, right_x):
            return
        
        layer = self.new_layer()
        for row_index in range(top_y, bottom_y):
            for column_index in range(left_x, right_x):
                layer[row_index][column_index] = fill_character
        self.layers.insert(0, layer)
        
    def find_first_hit_layer(self, select_x: int, select_y: int):
        for index in range(len(self.layers)):
            layer = self.layers[index]
            if layer[select_y][select_x] is not None:
                return index
        
    def DRAG_AND_DROP(self, select_x: int, select_y: int, release_x: int,  release_y:int):
        if not self.coordinate_is_within_bounds(select_y, select_x) or not self.coordinate_is_within_bounds(release_y, release_x):
            return
        
        hit_index = self.find_first_hit_layer(select_x, select_y)
        if hit_index is None:
            return
        
        layer = self.layers[hit_index]
        row_diff = release_y - select_y
        column_diff = release_x - select_x
        
        for row_index in range(self.row_size):
            new_row = row_index + row_diff
            for column_index in range(self.column_size):
                new_column = column_index + column_diff
                if not self.coordinate_is_within_bounds(new_row, new_column):
                    break
                
                if layer[row_index][column_index] is not None:
                    layer[new_row][new_column] = layer[row_index][column_index]
                    layer[row_index][column_index] = None
                
        self.layers[hit_index] = layer
        
        
    def ERASE_AREA(self, left_x: int, top_y: int, right_x: int, bottom_y:int):
        if not self.coordinate_is_within_bounds(top_y, left_x) or not self.coordinate_is_within_bounds(bottom_y, right_x):
            return
            
        for index in range(len(self.layers)):
            layer = self.layers[index]
            for row_index in range(top_y, bottom_y):
                for column_index in range(left_x, right_x):
                    layer[row_index][column_index] = None
            self.layers[index] = layer
            
        
    def BRING_TO_FRONT(self, select_x: int, select_y: int):
        if not self.coordinate_is_within_bounds(select_y, select_x):
            return
        
        hit_index = self.find_first_hit_layer(select_x, select_y)
        if hit_index is None:
            return
        
        layer = self.layers[hit_index]
        self.layers.remove(hit_index)
        self.layers.insert(0,layer)
        
        
    def PRINT_CANVAS(self):
        printable_layer = self.new_layer()
        
        for index in range(len(self.layers), -1, -1):
            layer = self.layers[index]
            for row_index in range(self.row_size):
                for column_index in range(self.column_size):
                    character = layer[row_index][column_index]
                    if character is not None:
                        printable_layer[row_index][column_index] = character
        
        return printable_layer


class Command(enum.IntEnum):
    DRAW_RECTANGLE = 0
    DRAG_AND_DROP = 1
    ERASE_AREA = 2
    BRING_TO_FRONT = 3
    PRINT_CANVAS = 4
    
    
class CommandWithArgs():
    command: Command
    args: List[Any]


class ASCIIPrinter:
    def print(self):
        canvas = Canvas()
        commands_with_args = self.read_commands()
        
        for c in commands_with_args:
            if c.command == Command.DRAW_RECTANGLE:
                canvas.DRAW_RECTANGLE(c.args)
            elif c.command == Command.DRAG_AND_DROP:
                canvas.DRAG_AND_DROP(c.args)
            elif c.command == Command.ERASE_AREA:
                canvas.ERASE_AREA(c.args)
            elif c.command == Command.BRING_TO_FRONT:
                canvas.BRING_TO_FRONT(c.args)
            elif c.command == Command.PRINT_CANVAS:
                canvas.PRINT_CANVAS(c.args)
            
        
    def read_commands() -> List[CommandWithArgs]:
        # some file reader with line parsing
        return []
