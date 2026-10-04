from math import hypot, sqrt

from hypothesis import given, strategies as st

from engine.math3d.vector3D import Vec3


float_strategy = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)
scalar_strategy = float_strategy
scalar_divisor_strategy = float_strategy.filter(lambda x: x != 0)


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector3d_add(x: float, y: float, z: float, ox: float, oy: float, oz: float):
    print(x, y, z, ox, oy, oz)
    vector = Vec3(x, y, z)
    other = Vec3(ox, oy, oz)
    expected = Vec3(x + ox, y + oy, z + oz)
    assert vector + other == expected
    assert other + vector == expected


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector3d_sub(x: float, y: float, z: float, ox: float, oy: float, oz: float):
    print(x, y, z, ox, oy, oz)
    vector = Vec3(x, y, z)
    other = Vec3(ox, oy, oz)
    assert vector - other == Vec3(x - ox, y - oy, z - oz)
    assert other - vector == Vec3(ox - x, oy - y, oz - z)


@given(float_strategy, float_strategy, float_strategy, scalar_strategy)
def test_vector3d_mul(x: float, y: float, z: float, scalar: float):
    print(x, y, z, scalar)
    vector = Vec3(x, y, z)
    expected = Vec3(x * scalar, y * scalar, z * scalar)
    assert vector * scalar == expected
    assert scalar * vector == expected


@given(float_strategy, float_strategy, float_strategy, scalar_divisor_strategy)
def test_vector3d_div(x: float, y: float, z: float, scalar: float):
    print(x, y, z, scalar)
    vector = Vec3(x, y, z)
    assert vector / scalar == Vec3(x / scalar, y / scalar, z / scalar)


@given(float_strategy, float_strategy, float_strategy)
def test_vector3d_neg(x: float, y: float, z: float):
    print(x, y, z)
    vector = Vec3(x, y, z)
    assert -vector == Vec3(-x, -y, -z)


@given(float_strategy, float_strategy, float_strategy)
def test_vector3d_length(x: float, y: float, z: float):
    print(x, y, z)
    vector = Vec3(x, y, z)
    assert vector.length() == hypot(x, y, z)


@given(float_strategy, float_strategy, float_strategy)
def test_vector3d_length_squared(x: float, y: float, z: float):
    print(x, y, z)
    vector = Vec3(x, y, z)
    assert vector.length_squared() == x * x + y * y + z * z


@given(float_strategy, float_strategy, float_strategy)
def test_vector3d_normalized(x: float, y: float, z: float):
    print(x, y, z)
    vector = Vec3(x, y, z)
    length_squared = vector.length_squared()

    if length_squared == 0:
        assert vector.normalized() == Vec3(0.0, 0.0, 0.0)
        return

    assert vector.normalized() == vector / sqrt(length_squared)


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector3d_dot(x: float, y: float, z: float, ox: float, oy: float, oz: float):
    print(x, y, z, ox, oy, oz)
    vector = Vec3(x, y, z)
    other = Vec3(ox, oy, oz)
    expected = x * ox + y * oy + z * oz
    assert vector.dot(other) == expected
    assert other.dot(vector) == expected


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector3d_cross(x: float, y: float, z: float, ox: float, oy: float, oz: float):
    print(x, y, z, ox, oy, oz)
    vector = Vec3(x, y, z)
    other = Vec3(ox, oy, oz)
    expected = Vec3(y * oz - z * oy, z * ox - x * oz, x * oy - y * ox)
    assert vector.cross(other) == expected


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_vector3d_distance_to(x: float, y: float, z: float, ox: float, oy: float, oz: float):
    print(x, y, z, ox, oy, oz)
    vector = Vec3(x, y, z)
    other = Vec3(ox, oy, oz)
    assert vector.distance_to(other) == hypot(x - ox, y - oy, z - oz)
