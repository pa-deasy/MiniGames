from domain.models.game_state import Board, MarkerPosition


def map_input_to_marker_position(input_message: str) -> MarkerPosition:
    try:
        split_input = input_message.split(',')
        return MarkerPosition(row_position=int(split_input[0]), column_position=int(split_input[1]))
    except:
        return MarkerPosition(row_position=Board.BOARD_AXIS_POINT, column_position=Board.BOARD_AXIS_POINT)