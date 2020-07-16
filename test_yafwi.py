from hypothesis import given
from hypothesis.strategies import integers, sampled_from
import pytest

from yafwi import *


@pytest.mark.parametrize('cls, expected', [
    (sbyte, int8),
    (byte, uint8),
    (short, int16),
    (ushort, uint16),
    (int_, int32),
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
    (int128, -170141183460469231731687303715884105728, 170141183460469231731687303715884105727),
    (uint128, 0, 340282366920938463463374607431768211455),
    (int256, -57896044618658097711785492504343953926634992332820282019728792003956564819968, 57896044618658097711785492504343953926634992332820282019728792003956564819967),
    (uint256, 0, 115792089237316195423570985008687907853269984665640564039457584007913129639935),
])
def test_limits(cls: FixedWidthInt, min_val: int, max_val: int):
    assert isinstance(cls.min, cls)
    assert cls.min == min_val
    assert isinstance(cls.max, cls)
    assert cls.max == max_val


@pytest.mark.parametrize('cls', [
    int8, uint8, int16, uint16, int32, uint32,
    int64, uint64, int128, uint128, int256, uint256,
])
def test_overflow(cls: FixedWidthInt):
    assert cls.max + 1 == cls.min
    assert cls.min - 1 == cls.max


@given(reference=sampled_from([int8, uint8, int16, uint16,
                               int32, uint32, int64, uint64]),
       value=integers(min_value=int(int64.min) * 100,
                      max_value=int(uint64.max) * 100))
def test_generated(reference, value):
    generated = generate(reference.width, reference.unsigned)
    assert generated(value) == reference(value)
