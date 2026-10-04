from math import hypot, sqrt

import pytest
from hypothesis import given, strategies as st

from engine.math3d.vector3D import Vec3
from engine.math3d.vector4D import Vec4


float_strategy = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)

scalar_strategy = float_strategy

scalar_divisor_strategy = float_strategy.filter(lambda x: x != 0)

non_zero_w_strategy = float_strategy.filter(lambda x: x != 0)


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector4d_add(x: float, y: float, z: float, w: float, ox: float, oy: float, oz: float, ow: float):
    vector = Vec4(x, y, z, w)
    other = Vec4(ox, oy, oz, ow)

    expected = Vec4(x + ox, y + oy, z + oz, w + ow)

    assert vector + other == expected
    assert other + vector == expected


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector4d_sub(x: float, y: float, z: float, w: float, ox: float, oy: float, oz: float, ow: float):
    vector = Vec4(x, y, z, w)
    other = Vec4(ox, oy, oz, ow)

    assert vector - other == Vec4(x - ox, y - oy, z - oz, w - ow)
    assert other - vector == Vec4(ox - x, oy - y, oz - z, ow - w)


@given(float_strategy, float_strategy, float_strategy, float_strategy, scalar_strategy)
def test_vector4d_mul(x: float, y: float, z: float, w: float, scalar: float):
    vector = Vec4(x, y, z, w)

    expected = Vec4(x * scalar, y * scalar, z * scalar, w * scalar)

    assert vector * scalar == expected
    assert scalar * vector == expected


@given(float_strategy, float_strategy, float_strategy, float_strategy, scalar_divisor_strategy)
def test_vector4d_div(x: float, y: float, z: float, w: float, scalar: float):
    vector = Vec4(x, y, z, w)

    assert vector / scalar == Vec4(x / scalar, y / scalar, z / scalar, w / scalar)


def test_vector4d_div_zero():
    vector = Vec4(1.0, 2.0, 3.0, 4.0)

    with pytest.raises(ZeroDivisionError):
        vector / 0


@given(float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector4d_neg(x: float, y: float, z: float, w: float):
    vector = Vec4(x, y, z, w)

    assert -vector == Vec4(-x, -y, -z, -w)


@given(float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector4d_length(x: float, y: float, z: float, w: float):
    vector = Vec4(x, y, z, w)

    assert vector.length() == hypot(x, y, z, w)


@given(float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector4d_length_squared(x: float, y: float, z: float, w: float):
    vector = Vec4(x, y, z, w)

    assert vector.length_squared() == x * x + y * y + z * z + w * w


@given(float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector4d_normalized(x: float, y: float, z: float, w: float):
    vector = Vec4(x, y, z, w)
    length_squared = vector.length_squared()

    if length_squared == 0:
        assert vector.normalized() == Vec4(0.0, 0.0, 0.0, 0.0)
        return

    assert vector.normalized() == vector / sqrt(length_squared)


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector4d_dot(x: float, y: float, z: float, w: float, ox: float, oy: float, oz: float, ow: float):
    vector = Vec4(x, y, z, w)
    other = Vec4(ox, oy, oz, ow)

    expected = x * ox + y * oy + z * oz + w * ow

    assert vector.dot(other) == expected
    assert other.dot(vector) == expected


@given(float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector4d_from_vec3(x: float, y: float, z: float, w: float):
    vector = Vec3(x, y, z)

    result = Vec4.from_vec3(vector, w)

    assert result == Vec4(x, y, z, w)


@given(float_strategy, float_strategy, float_strategy)
def test_vector4d_from_vec3_default_w(x: float, y: float, z: float):
    vector = Vec3(x, y, z)

    assert Vec4.from_vec3(vector) == Vec4(x, y, z, 1.0)


@given(float_strategy, float_strategy, float_strategy, non_zero_w_strategy)
def test_vector4d_to_vec3(x: float, y: float, z: float, w: float):
    vector = Vec4(x, y, z, w)

    assert vector.to_vec3() == Vec3(x / w, y / w, z / w)


def test_vector4d_to_vec3_zero_w():
    vector = Vec4(1.0, 2.0, 3.0, 0.0)

    with pytest.raises(ValueError):
        vector.to_vec3()