import vestaboard
import pytest

def test_installable_with_no_params_errors():
    with pytest.raises(ValueError):
        i = vestaboard.Installable()
