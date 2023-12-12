import pytest
from src.domain.models.game_state import GameState, MarkerPosition, PlayerMarker

from src.domain.tic_tac_toe import INVALID_MOVE_REASON_GAME_WON, INVALID_MOVE_REASON_POSITION_INCORRECT, INVALID_MOVE_REASON_POSITION_OCCUPIED, INVALID_MOVE_REASON_WRONG_TURN, start_game, validate_move, place_marker


def test_start_game_when_started_then_sets_up_state():
    game_state = start_game()
    
    assert game_state.player_turn.name == PlayerMarker.X.name
    assert game_state.board is not None
    
    
def test_validate_move_when_position_available_then_is_valid():
    game_state = GameState()
    marker_position = MarkerPosition(row_position=1, column_position=1)
    player_marker = PlayerMarker.X
    
    move_validation = validate_move(game_state, marker_position, player_marker)
    
    assert move_validation.is_valid == True
    

def test_validate_move_when_position_is_not_available_then_is_invalid():
    game_state = GameState()
    game_state.board.set_player_marker(MarkerPosition(row_position=1, column_position=1), PlayerMarker.X)
    game_state.player_turn = PlayerMarker.O
    player_marker = PlayerMarker.O
    marker_position = MarkerPosition(row_position=1, column_position=1)
    
    move_validation = validate_move(game_state, marker_position, player_marker)
    
    assert move_validation.is_valid == False
    assert move_validation.reason == INVALID_MOVE_REASON_POSITION_OCCUPIED
    

def test_validate_move_when_position_is_not_on_board_then_is_invalid():
    game_state = GameState()
    marker_position = MarkerPosition(row_position=0, column_position=0)
    player_marker = PlayerMarker.X
    
    move_validation = validate_move(game_state, marker_position, player_marker)
    
    assert move_validation.is_valid == False
    assert move_validation.reason == INVALID_MOVE_REASON_POSITION_INCORRECT
    

def test_validate_move_when_not_players_turn_then_is_invalid():
    game_state = GameState()
    marker_position = MarkerPosition(row_position=1, column_position=1)
    player_marker = PlayerMarker.O
    
    move_validation = validate_move(game_state, marker_position, player_marker)
    
    assert move_validation.is_valid == False
    assert move_validation.reason == INVALID_MOVE_REASON_WRONG_TURN
    

def test_validate_move_when_game_won_then_is_invalid():
    game_state = GameState()
    game_state.is_won = True
    marker_position = MarkerPosition(row_position=1, column_position=1)
    player_marker = PlayerMarker.X
    
    move_validation = validate_move(game_state, marker_position, player_marker)
    
    assert move_validation.is_valid == False
    assert move_validation.reason == INVALID_MOVE_REASON_GAME_WON
    
    
def test_place_marker_when_x_placed_then_is_successful():
    game_state = GameState()
    marker_position = MarkerPosition(row_position=1, column_position=1)
    player_marker = PlayerMarker.X
    
    updated_game_state = place_marker(game_state, marker_position, player_marker)
    
    assert updated_game_state.board.get_player_marker(marker_position).name == player_marker.name
    assert updated_game_state.player_turn.name == PlayerMarker.O.name
    
    
def test_place_marker_when_o_placed_then_is_successful():
    game_state = GameState()
    game_state.board.set_player_marker(MarkerPosition(row_position=1, column_position=1), PlayerMarker.X)
    game_state.player_turn = PlayerMarker.O
    player_marker = PlayerMarker.O
    marker_position = MarkerPosition(row_position=1, column_position=2)
    
    updated_game_state = place_marker(game_state, marker_position, player_marker)
    
    assert updated_game_state.board.get_player_marker(marker_position) == player_marker
    assert updated_game_state.player_turn.name == PlayerMarker.X.name
    
    
def test_place_marker_when_game_won_then_returns_is_won():
    game_state = GameState()
    game_state = place_marker(game_state, MarkerPosition(row_position=1, column_position=1), PlayerMarker.X)
    assert game_state.is_won == False
    
    game_state = place_marker(game_state, MarkerPosition(row_position=2, column_position=2), PlayerMarker.X)
    assert game_state.is_won == False
    
    game_state = place_marker(game_state, MarkerPosition(row_position=3, column_position=3), PlayerMarker.X)
    assert game_state.is_won == True
