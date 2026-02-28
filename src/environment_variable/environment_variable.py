import os
from typing import Callable, TypeVar

from .boolean import str_to_bool
from .exceptions import SecretValueError

T = TypeVar("T")


class EnvironmentVariable:
    """Utility class to manage environment variables with type conversion and default values.

    Args:
        name (str): The name of the environment variable.
        type_ (Callable[[str], T]): The type or conversion function
            to convert the environment variable's string value to the desired type.
        default_value (T | None): The default value to return if the environment variable is not
            set.

    Raises:
        ValueError: If the conversion of the environment variable's value fails.

    Example usage:
        >>> env_var = EnvironmentVariable("MY_ENV_VAR", int, 42)
        >>> env_var.get()
        42
        >>> env_var.set(10)
        >>> env_var.get()
        10
        >>> env_var.unset()
        >>> env_var.get()
        42
        import os
        >>> os.environ["MY_ENV_VAR"] = "100"
        >>> env_var.get()
        100
        >>> env_var.set(42)
        >>> os.environ["MY_ENV_VAR"]
        '42'
    """

    def __init__(
        self,
        name: str,
        type_: Callable[[str], T],
        default_value: T | None = None,
        *,
        obfuscated: bool = False,
    ):
        """Initialize an EnvironmentVariable instance.

        Args:
            name (str): The name of the environment variable.
            type_ (Callable[[str], T]): The type or conversion function
                to convert the environment variable's string value to the desired type.
            default_value (T | None): The default value to return if the environment variable is not
                set.
            obfuscated (bool): If True, the variable's value will be obfuscated when accessed.

        """
        # Special handling for bool type
        # Takes care of commons string representations of booleans
        if type_ is bool:
            type_ = str_to_bool
        self.name = name
        self.type_ = type_
        self.default_value = default_value
        self.obfuscated = obfuscated

    @property
    def is_set(self) -> bool:
        return self.name in os.environ

    def get_raw(self) -> str | None:
        return os.getenv(self.name, None)

    def set(self, value):
        os.environ[self.name] = str(value)

    def unset(self):
        os.environ.pop(self.name, None)

    def get(self) -> T | None:
        val = self.get_raw()
        if val is not None:
            try:
                return self.type_(val)
            except Exception as e:
                msg = self._conversion_error_msg(val)
                if self.obfuscated:
                    raise SecretValueError(msg)
                raise ValueError(msg) from e
        return self.default_value

    def _conversion_error_msg(self, val) -> str:
        return f"Failed to convert {self._printable_value(val)!r} for {self.name}"

    def _printable_value(self, value) -> str:
        if self.obfuscated:
            return "*****"
        return str(value)

    def __str__(self):
        return f"{self.name} (default: {self._printable_value(self.default_value)})"

    def __repr__(self):
        return repr(self.name)


__all__ = ["EnvironmentVariable"]
