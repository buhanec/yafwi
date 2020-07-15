"""Yet another fixed with integer."""

__all__ = ('FixedWidthInt', 'int8', 'int16', 'int32', 'int64', 'uint8',
           'uint16', 'uint32', 'uint64', 'sbyte', 'byte', 'short',
           'ushort', 'sint', 'uint', 'long', 'ulong')


from functools import wraps
from typing import Protocol, Tuple
from ctypes import (c_int8, c_int16, c_int32, c_int64,
                    c_uint8, c_uint16, c_uint32, c_uint64)

# TODO: Docs
# TODO: Comparison improvements


class CTypeInt(Protocol):
    value: int

    def _init_(self, value: int) -> None:
        ...


class FixedWidthInt(type):
    _raw: CTypeInt
    _width: int
    _unsigned: bool

    @property
    def width(cls) -> int:
        return cls._width

    @property
    def unsigned(cls) -> bool:
        return cls._unsigned

    @property
    def max(cls) -> int:
        if cls.unsigned:
            return cls(2 ** cls._width - 1)
        return cls(2 ** (cls._width - 1) - 1)

    @property
    def min(cls) -> int:
        if cls.unsigned:
            return cls(0)
        return cls(-(2 ** (cls._width - 1)))


def take_wider(fn):
    @wraps(fn)
    def wrapper(self: 'BaseFixedWidthInt', other: int):
        if (isinstance(other, BaseFixedWidthInt)
                and (other.width > self.width
                     or other.width == self.width
                     and other.unsigned
                     and not self.unsigned)):
            return NotImplemented
        return fn(self, other)

    return wrapper


class BaseFixedWidthInt(int, metaclass=FixedWidthInt):

    def __new__(cls, value: int) -> int:
        if cls is BaseFixedWidthInt:
            raise RuntimeError('Use concrete implementation, not base _Int')
        # noinspection PyArgumentList,PyUnresolvedReferences
        return int.__new__(cls, cls._raw(value).value)

    @property
    def width(self) -> int:
        # noinspection PyTypeChecker
        return type(self).width

    @property
    def unsigned(self) -> bool:
        # noinspection PyTypeChecker
        return type(self).unsigned

    @property
    def max(self) -> int:
        # noinspection PyTypeChecker
        return type(self).max

    @property
    def min(self) -> int:
        # noinspection PyTypeChecker
        return type(self).min

    # Absolute value

    def __abs__(self) -> int:
        return type(self)(super().__abs__())

    # Addition

    @take_wider
    def __add__(self, other: int) -> int:
        return type(self)(super().__add__(other))

    @take_wider
    def __radd__(self, other: int) -> int:
        return type(self)(super().__radd__(other))

    # And

    @take_wider
    def __and__(self, other: int) -> int:
        return type(self)(super().__and__(other))

    @take_wider
    def __rand__(self, other: int) -> int:
        return type(self)(super().__rand__(other))

    # Division

    def __divmod__(self, other: int) -> Tuple[int, int]:
        div, mod = super().__divmod__(other)
        return type(self)(div), type(self)(mod)

    def __floordiv__(self, other: int) -> int:
        return type(self)(super().__floordiv__(other))

    def __mod__(self, other: int) -> int:
        return type(self)(super().__mod__(other))

    # Identities

    def __ceil__(self) -> int:
        return type(self)(self)

    def __floor__(self) -> int:
        return type(self)(self)

    def __index__(self) -> int:
        return type(self)(self)

    def __int__(self) -> int:
        return type(self)(self)

    def __trunc__(self) -> int:
        return type(self)(self)

    def __round__(self, n=None):
        return type(self)(super().__round__(n))

    # Pos

    def __pos__(self) -> int:
        return type(self)(super().__pos__())

    # Neg

    def __invert__(self) -> int:
        return type(self)(super().__invert__())

    def __neg__(self) -> int:
        return type(self)(super().__neg__())

    # Shifting

    def __lshift__(self, other: int) -> int:
        return type(self)(super().__lshift__(other))

    def __rshift__(self, other: int) -> int:
        return type(self)(super().__rshift__(other))

    # Multiplication

    @take_wider
    def __mul__(self, other: int) -> int:
        return type(self)(super().__mul__(other))

    @take_wider
    def __rmul__(self, other: int) -> int:
        return type(self)(super().__rmul__(other))

    # Or

    @take_wider
    def __or__(self, other: int) -> int:
        return type(self)(super().__or__(other))

    @take_wider
    def __ror__(self, other: int) -> int:
        return type(self)(super().__ror__(other))

    # Exp

    def __pow__(self, power: int, modulo=None):
        return type(self)(super().__pow__(power, modulo))

    # Subtract

    @take_wider
    def __sub__(self, other: int) -> int:
        return type(self)(super().__sub__(other))

    @take_wider
    def __rsub__(self, other: int) -> int:
        return type(self)(super().__rsub__(other))

    # XOR

    @take_wider
    def __xor__(self, other: int) -> int:
        return type(self)(super().__xor__(other))

    @take_wider
    def __rxor__(self, other: int) -> int:
        return type(self)(super().__rxor__(other))

    # Hash

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        if self.unsigned:
            prefix = 'u'
        else:
            prefix = ''
        return f'{prefix}int{self.width}({super().__repr__()})'


# noinspection PyPep8Naming
class int8(BaseFixedWidthInt):
    _raw = c_int8
    _width = 8
    _unsigned = False


# noinspection PyPep8Naming
class int16(BaseFixedWidthInt):
    _raw = c_int16
    _width = 16
    _unsigned = False


# noinspection PyPep8Naming
class int32(BaseFixedWidthInt):
    _raw = c_int32
    _width = 32
    _unsigned = False


# noinspection PyPep8Naming
class int64(BaseFixedWidthInt):
    _raw = c_int64
    _width = 64
    _unsigned = False


# noinspection PyPep8Naming
class uint8(BaseFixedWidthInt):
    _raw = c_uint8
    _width = 8
    _unsigned = True


# noinspection PyPep8Naming
class uint16(BaseFixedWidthInt):
    _raw = c_uint16
    _width = 16
    _unsigned = True


# noinspection PyPep8Naming
class uint32(BaseFixedWidthInt):
    _raw = c_uint32
    _width = 32
    _unsigned = True


# noinspection PyPep8Naming
class uint64(BaseFixedWidthInt):
    _raw = c_uint64
    _width = 64
    _unsigned = True


# Aliases
sbyte = int8
byte = uint8
short = int16
ushort = uint16
sint = int32  # Don't want to override "int"
uint = uint32
long = int64
ulong = uint64
