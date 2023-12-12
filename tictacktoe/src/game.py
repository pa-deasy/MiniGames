from console import print_message, print_message_and_get_input
from domain.models.game_state import PlayerMarker, GameState, Board, MarkerPosition
from domain.models.mapping import map_input_to_marker_position
from domain.tic_tac_toe import place_marker, validate_move


def run():
    game_state = GameState()    
    _print_game_start()
    
    player_turn: PlayerMarker
    while not game_state.is_won:
        player_turn = game_state.player_turn
        _print_board(game_state.board)
        input_message = _get_player_move(player_turn)
        marker_position = map_input_to_marker_position(input_message)
        
        move_validation = validate_move(game_state, marker_position, player_turn)
        if not move_validation.is_valid:
            _print_invalid_move(move_validation.reason)
            continue
        
        game_state = place_marker(game_state, marker_position, player_turn)
    
    _print_board(game_state.board)
    _print_game_won(player_turn)
    
        
        
def _print_game_start() -> None:
    message = 'New game of Tic Tac Toe'
    print_message(message)
    

def _print_board(board: Board) -> None:
    message = '---------------\n'
    for row in board.value:
        for player_marker in row:
            if player_marker is None:
                message += '|   |'
            else:
                message += f'| {player_marker.name} |'
                
        message += '\n---------------\n'
    print_message(message)
    

def _get_player_move(player_marker: PlayerMarker) -> str:
    message = f'It is player {player_marker.name}\'s turn'
    message += '\nPlease input a move within the range 1,1 to 3,3\n:'
    input_message = print_message_and_get_input(message)
    return input_message


def _print_invalid_move(reason: str) -> None:
    message = 'Invalid move please try again\n'
    message += reason
    print_message(message)
    
    
def _print_game_won(player_marker: PlayerMarker) -> None:
    message = f'Player {player_marker} has won\n'
    message += 'Game over!'
    print_message(message)

    
if __name__ == "__main__":
    run()
