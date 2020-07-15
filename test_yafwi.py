import pytest
import hypothesis

from yafwi import *


@pytest.mark.parametrize('cls, expected', [
    (sbyte, int8),
    (byte, uint8),
    (short, int16),
    (ushort, uint16),
    (sint, int32),
    (uint, uint32),
    (long, int64),
    (ulong, uint64),
])
def test_aliases(cls: FixedWidthInt, expected: FixedWidthInt):
    assert cls is expected


@pytest.mark.parametrize('val, other, expected', [
    (int8(-128), -128, True),
    (int8(127), 127, True),
])
def test_equality(val: FixedWidthInt, other: int, expected: bool):
    assert (val == other) is expected


@pytest.mark.parametrize('cls, min_val, max_val', [
    (int8, -128, 127),
    (uint8, 0, 255),
    (int16, -32768, 32767),
    (uint16, 0, 65535),
    (int32, -2147483648, 2147483647),
    (uint32, 0, 4294967295),
    (int64, -9223372036854775808, 9223372036854775807),
    (uint64, 0, 18446744073709551615),
])
def test_limits(cls: FixedWidthInt, min_val: int, max_val: int):
    assert isinstance(cls.min, cls)
    assert cls.min == min_val
    assert isinstance(cls.max, cls)
    assert cls.max == max_val
