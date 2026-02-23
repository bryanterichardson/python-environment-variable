import os

import pytest

from environment_variable import EnvironmentVariable, SecretValueError


def test_get_default_when_not_set():
    env_var = EnvironmentVariable("TEST_VAR", str, "default")
    assert env_var.get() == "default"


def test_get_from_environment(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "value")
    env_var = EnvironmentVariable("TEST_VAR", str, "default")
    assert env_var.get() == "value"


def test_set_value(monkeypatch):
    env_var = EnvironmentVariable("TEST_VAR", str, "default")
    env_var.set("new_value")
    assert env_var.get() == "new_value"
    assert os.environ["TEST_VAR"] == "new_value"


def test_unset_value(monkeypatch):
    env_var = EnvironmentVariable("TEST_VAR", str, "default")
    env_var.set("value")
    env_var.unset()
    assert env_var.get() == "default"
    assert "TEST_VAR" not in os.environ


def test_is_set(monkeypatch):
    env_var = EnvironmentVariable("TEST_VAR", str, "default")
    assert not env_var.is_set
    monkeypatch.setenv("TEST_VAR", "value")
    assert env_var.is_set
    monkeypatch.delenv("TEST_VAR")
    assert not env_var.is_set


def test_int_conversion(monkeypatch):
    monkeypatch.setenv("TEST_INT", "42")
    env_var = EnvironmentVariable("TEST_INT", int, 0)
    assert env_var.get() == 42


def test_bool_conversion_true(monkeypatch):
    monkeypatch.setenv("TEST_BOOL", "true")
    env_var = EnvironmentVariable("TEST_BOOL", bool, False)
    assert env_var.get() is True


def test_bool_conversion_false(monkeypatch):
    monkeypatch.setenv("TEST_BOOL", "false")
    env_var = EnvironmentVariable("TEST_BOOL", bool, True)
    assert env_var.get() is False


def test_invalid_conversion_raises_error(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "not_a_number")
    env_var = EnvironmentVariable("TEST_VAR", int, 0)
    with pytest.raises(ValueError, match="Failed to convert"):
        env_var.get()


def test_get_raw(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "42")
    env_var = EnvironmentVariable("TEST_VAR", int, 0)
    assert env_var.get_raw() == "42"


def test_get_raw_not_set():
    env_var = EnvironmentVariable("TEST_VAR", str, "default")
    assert env_var.get_raw() is None


def test_custom_conversion_function(monkeypatch):
    def custom_convert(val: str) -> list:
        return val.split(",")

    monkeypatch.setenv("TEST_VAR", "a,b,c")
    env_var = EnvironmentVariable("TEST_VAR", custom_convert, [])
    assert env_var.get() == ["a", "b", "c"]


def test_logs_obfuscate_default_value():
    env_var = EnvironmentVariable("TEST_VAR", str, "sensitive_value", obfuscated=True)
    val = str(env_var)
    assert "sensitive_value" not in val
    assert "****" in val


def test_returns_non_obfuscated_value_from_get():
    env_var = EnvironmentVariable("TEST_VAR", str, "sensitive_value", obfuscated=True)
    assert env_var.get() == "sensitive_value"


def test_obfuscated_values_upon_parsing_failures(monkeypatch):
    value = "super-secret-value"
    test_var_name = "TEST_SECRET_VAR"
    monkeypatch.setenv(test_var_name, value)

    with pytest.raises(SecretValueError) as exc_info:
        ev = EnvironmentVariable(test_var_name, int, None, obfuscated=True)
        ev.get()
    assert value not in str(exc_info.value)
