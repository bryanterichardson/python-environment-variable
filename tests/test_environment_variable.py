import os

import pytest

from environment_variable import EnvironmentVariable, SecretValueError

TEST_VAR_NAME = "_TEST_VAR"


def test_get_default_when_not_set(monkeypatch):
    default_value = "some-default-value"
    monkeypatch.delenv(TEST_VAR_NAME, raising=False)
    env_var = EnvironmentVariable(TEST_VAR_NAME, str, default_value)
    assert env_var.get() == default_value


def test_get_from_environment(monkeypatch):
    default_value = "some-default-value"
    test_value = "some-other-value-that-is-not-default"
    monkeypatch.setenv(TEST_VAR_NAME, test_value)
    env_var = EnvironmentVariable(TEST_VAR_NAME, str, default_value)
    assert env_var.get() == test_value


@pytest.mark.parametrize("exists", [True, False])
def test_set_value(exists: bool, monkeypatch):
    value_to_set = "some-initial-value"
    if exists:
        monkeypatch.setenv(TEST_VAR_NAME, "some-existing-value-to-overwrite")
    else:
        monkeypatch.delenv(TEST_VAR_NAME, raising=False)
    env_var = EnvironmentVariable(TEST_VAR_NAME, str)
    env_var.set(value_to_set)
    assert env_var.get() == value_to_set
    assert os.environ[TEST_VAR_NAME] == value_to_set


def test_unset_value(monkeypatch):
    default_value = "some-default-value"
    value_to_set = "some-initial-value"
    env_var = EnvironmentVariable(TEST_VAR_NAME, str, default_value)
    env_var.set(value_to_set)
    env_var.unset()
    assert env_var.get() == default_value
    assert TEST_VAR_NAME not in os.environ


def test_is_set(monkeypatch):
    env_var = EnvironmentVariable(TEST_VAR_NAME, str, "default")
    assert not env_var.is_set
    monkeypatch.setenv(TEST_VAR_NAME, "value")
    assert env_var.is_set
    monkeypatch.delenv(TEST_VAR_NAME)
    assert not env_var.is_set


@pytest.mark.parametrize(
    "as_type,value,expected",
    [
        (int, "42", 42),
        (float, "3.14", 3.14),
        (str, "hello", "hello"),
        (bool, "0", False),
        (bool, "false", False),
        (bool, "FALSE", False),
        (bool, "False", False),
        (bool, "NO", False),
        (bool, "no", False),
        (bool, "No", False),
        (bool, "Off", False),
        (bool, "OFF", False),
        (bool, "off", False),
        (bool, "1", True),
        (bool, "true", True),
        (bool, "TRUE", True),
        (bool, "True", True),
        (bool, "yes", True),
        (bool, "YES", True),
        (bool, "Yes", True),
        (bool, "on", True),
        (bool, "ON", True),
        (bool, "On", True),
        # "Type" can be arbitrary Callable[[str], T]
        (lambda s: s.split(":")[1], "This:value", "value"),
        (lambda s: s.split(","), "a,b,c", ["a", "b", "c"]),
    ],
)
def test_type_conversion(monkeypatch, as_type, value: str, expected):
    monkeypatch.setenv(TEST_VAR_NAME, value)
    env_var = EnvironmentVariable(TEST_VAR_NAME, as_type, value)
    assert env_var.get_raw() == value
    assert env_var.get() == expected


def test_invalid_conversion_raises_error(monkeypatch):
    monkeypatch.setenv(TEST_VAR_NAME, "not_a_number")
    env_var = EnvironmentVariable(TEST_VAR_NAME, int, 0)
    with pytest.raises(ValueError, match="Failed to convert"):
        env_var.get()


def test_get_raw(monkeypatch):
    monkeypatch.setenv(TEST_VAR_NAME, "42")
    env_var = EnvironmentVariable(TEST_VAR_NAME, int, 0)
    assert env_var.get_raw() == "42"


def test_get_raw_not_set():
    env_var = EnvironmentVariable(TEST_VAR_NAME, str, "default")
    assert env_var.get_raw() is None


def test_logs_obfuscate_default_value():
    value = "sensitive_value"
    env_var = EnvironmentVariable(TEST_VAR_NAME, str, value, obfuscated=True)
    assert value not in str(env_var)
    assert value not in repr(env_var)


def test_returns_non_obfuscated_value_from_get():
    value = "sensitive_value"
    env_var = EnvironmentVariable(TEST_VAR_NAME, str, value, obfuscated=True)
    assert env_var.get() == value
    assert value not in str(env_var)
    assert value not in repr(env_var)


def test_obfuscated_values_upon_parsing_failures(monkeypatch):
    value = "super-secret-value"
    monkeypatch.setenv(TEST_VAR_NAME, value)

    with pytest.raises(SecretValueError) as exc_info:
        env_var = EnvironmentVariable(TEST_VAR_NAME, int, obfuscated=True)
        env_var.get()
    assert value not in str(exc_info.value)
