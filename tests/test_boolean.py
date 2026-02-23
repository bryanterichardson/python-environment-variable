import pytest

from environment_variable.boolean import _FALSY, _TRUTHY, str_to_bool


@pytest.mark.parametrize(
    "value, expected",
    [
        ("false", False),
        ("0", False),
        ("no", False),
        ("off", False),
        ("true", True),
        ("1", True),
        ("yes", True),
        ("on", True),
    ],
)
def test_str_to_bool_is_case_insensitive_with_expected_output(value: str, expected: bool):
    assert str_to_bool(value.upper()) is expected
    assert str_to_bool(value.lower()) is expected
    assert str_to_bool(value.capitalize()) is expected


def test_str_to_bool_give_back_the_right_bool():
    for truthy in _TRUTHY:
        assert str_to_bool(truthy) is True
        assert str_to_bool(truthy.upper()) is True
        assert str_to_bool(truthy.capitalize()) is True
        assert str_to_bool(truthy.lower()) is True
    for falsy in _FALSY:
        assert str_to_bool(falsy) is False
        assert str_to_bool(falsy.upper()) is False
        assert str_to_bool(falsy.capitalize()) is False
        assert str_to_bool(falsy.lower()) is False


def test_str_to_bool_raises_value_error_on_invalid_input():
    invalid_inputs = ["maybe", "2", "yesno", "truth", "falsity", "", " ", "123", "onoff"]
    for invalid in invalid_inputs:
        with pytest.raises(ValueError):
            str_to_bool(invalid)
