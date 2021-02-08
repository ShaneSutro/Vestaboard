import vestaboard
import pytest

def test_installable_with_no_params_errors():
    with pytest.raises(ValueError):
        vestaboard.Installable()

def test_board_instance_fails_with_no_file():
    with pytest.raises(ValueError):
        vestaboard.Board()
