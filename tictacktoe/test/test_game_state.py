import pytest

from src.domain.models.game_state import Board, GameState, MarkerPosition, PlayerMarker


def test_marker_position_when_inside_of_board_then_returns_false():
    marker_position = MarkerPosition(row_position=1, column_position=1)
    
    is_outside_of_board = marker_position.is_outside_of_board()
    
    assert is_outside_of_board == False


def test_marker_position_when_outside_of_board_then_returns_true():
    marker_position = MarkerPosition(row_position=0, column_position=0)
    
    is_outside_of_board = marker_position.is_outside_of_board()
    
    assert is_outside_of_board == True


def test_board_when_set_up_then_empty_board_present():
    board = Board()

    assert len(board.value) == Board.BOARD_SIZE
    assert len(board.value) == Board.BOARD_SIZE
    assert board.get_player_marker(MarkerPosition(row_position=1, column_position=1)) == None
    assert board.get_player_marker(MarkerPosition(row_position=3, column_position=3)) == None
    

def test_board_when_set_and_get_player_marker_then_returns_marker():
    board = Board()
    marker_position = MarkerPosition(row_position=1, column_position=1)
    player_marker = PlayerMarker.X
    board.set_player_marker(marker_position, player_marker)
    
    actual_player_marker = board.get_player_marker(marker_position)

    assert actual_player_marker == player_marker
    

def test_board_when_winning_top_horizontal_line_then_returns_true():
    board = Board()
    board.set_player_marker(MarkerPosition(row_position=1, column_position=1), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=1, column_position=2), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=1, column_position=3), PlayerMarker.X)
    
    has_winning_line = board.has_winning_line()

    assert has_winning_line == True
    

def test_board_when_winning_bottom_horizontal_line_then_returns_true():
    board = Board()
    board.set_player_marker(MarkerPosition(row_position=3, column_position=1), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=3, column_position=2), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=3, column_position=3), PlayerMarker.X)
    
    has_winning_line = board.has_winning_line()

    assert has_winning_line == True
    
    
def test_board_when_winning_left_vertical_line_then_returns_true():
    board = Board()
    board.set_player_marker(MarkerPosition(row_position=1, column_position=1), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=2, column_position=1), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=3, column_position=1), PlayerMarker.X)
    
    has_winning_line = board.has_winning_line()

    assert has_winning_line == True
    

def test_board_when_winning_right_vertical_line_then_returns_true():
    board = Board()
    board.set_player_marker(MarkerPosition(row_position=1, column_position=3), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=2, column_position=3), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=3, column_position=3), PlayerMarker.X)
    
    has_winning_line = board.has_winning_line()

    assert has_winning_line == True
    

def test_board_when_winning_left_diagonal_line_then_returns_true():
    board = Board()
    board.set_player_marker(MarkerPosition(row_position=1, column_position=1), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=2, column_position=2), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=3, column_position=3), PlayerMarker.X)
    
    has_winning_line = board.has_winning_line()

    assert has_winning_line == True
    

def test_board_when_winning_right_diagonal_line_then_returns_true():
    board = Board()
    board.set_player_marker(MarkerPosition(row_position=1, column_position=3), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=2, column_position=2), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=3, column_position=1), PlayerMarker.X)
    
    has_winning_line = board.has_winning_line()

    assert has_winning_line == True
    
    
def test_board_when_no_winning_line_then_returns_false():
    board = Board()
    board.set_player_marker(MarkerPosition(row_position=1, column_position=1), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=2, column_position=2), PlayerMarker.X)
    board.set_player_marker(MarkerPosition(row_position=3, column_position=3), PlayerMarker.O)
    
    has_winning_line = board.has_winning_line()

    assert has_winning_line == False


def test_game_state_when_set_up_then_empty_board_present():
    game_state = GameState()

    assert game_state.player_turn == PlayerMarker.X
    assert len(game_state.board.value) == Board.BOARD_SIZE
    