from dataclasses import dataclass
from domain.models.game_state import Board, GameState, MarkerPosition, PlayerMarker

INVALID_MOVE_REASON_POSITION_OCCUPIED = 'Marker already placed in this position'
INVALID_MOVE_REASON_POSITION_INCORRECT = 'Marker is not within the board'
INVALID_MOVE_REASON_WRONG_TURN = 'It is not this players turn'
INVALID_MOVE_REASON_GAME_WON = 'The game is already won'
VALID_MOVE_REASON = 'This move is perfectly valid'

@dataclass
class MoveValidition:
    is_valid: bool
    reason: str


def start_game() -> GameState:
    return GameState()


def validate_move(game_state: GameState, marker_position: MarkerPosition, player_marker: PlayerMarker) -> MoveValidition:
    if game_state.board.get_player_marker(marker_position) is not None:
        return MoveValidition(is_valid=False, reason=INVALID_MOVE_REASON_POSITION_OCCUPIED)
    elif marker_position.is_outside_of_board():
        return MoveValidition(is_valid=False, reason=INVALID_MOVE_REASON_POSITION_INCORRECT)
    elif player_marker != game_state.player_turn:
        return MoveValidition(is_valid=False, reason=INVALID_MOVE_REASON_WRONG_TURN)
    elif game_state.is_won:
        return MoveValidition(is_valid=False, reason=INVALID_MOVE_REASON_GAME_WON)
    else:
        return MoveValidition(is_valid=True, reason=VALID_MOVE_REASON)


def place_marker(game_state: GameState, marker_position: MarkerPosition, player_marker: PlayerMarker) -> GameState:
    game_state.board.set_player_marker(marker_position, player_marker)
    game_state.player_turn = PlayerMarker.O if player_marker.name == PlayerMarker.X.name else PlayerMarker.X
    game_state.is_won = game_state.board.has_winning_line()
    
    return game_state
