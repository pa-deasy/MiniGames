import pytest

from src.domain.models.mapping import map_input_to_marker_position


def test_map_input_to_marker_position_when_valid_input_then_mapped():
    marker_position = map_input_to_marker_position('2,1')
    
    assert marker_position.row_position == 2
    assert marker_position.column_position == 1
    

def test_map_input_to_marker_position_when_invalid_input_then_default_mapped():
    marker_position = map_input_to_marker_position('bloop')
    
    assert marker_position.row_position == 0
    assert marker_position.column_position == 0
