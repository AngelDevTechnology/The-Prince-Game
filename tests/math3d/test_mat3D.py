import math

import pytest
from hypothesis import given, strategies as st

from engine.math3d.mat3D import Mat3
from engine.math3d.vector3D import Vec3


float_strategy = st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)

integer_strategy = st.integers(min_value=-10, max_value=10)

angle_strategy = st.floats(min_value=-2 * math.pi, max_value=2 * math.pi, allow_nan=False, allow_infinity=False)


def assert_mat3_close(actual: Mat3, expected: Mat3):
    assert math.isclose(actual.m00, expected.m00, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m01, expected.m01, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m02, expected.m02, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m10, expected.m10, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m11, expected.m11, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m12, expected.m12, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m20, expected.m20, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m21, expected.m21, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m22, expected.m22, rel_tol=1e-9, abs_tol=1e-9)


def test_mat3_identity():
    assert Mat3.identity() == Mat3(1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)


@given(float_strategy, float_strategy, float_strategy)
def test_mat3_identity_transform(x: float, y: float, z: float):
    matrix = Mat3.identity()
    vector = Vec3(x, y, z)

    assert matrix @ vector == vector


@given(angle_strategy)
def test_mat3_rotation_x(angle: float):
    matrix = Mat3.rotation_x(angle)
    c = math.cos(angle)
    s = math.sin(angle)

    assert matrix == Mat3(1.0, 0.0, 0.0, 0.0, c, -s, 0.0, s, c)


@given(angle_strategy)
def test_mat3_rotation_y(angle: float):
    matrix = Mat3.rotation_y(angle)
    c = math.cos(angle)
    s = math.sin(angle)

    assert matrix == Mat3(c, 0.0, s, 0.0, 1.0, 0.0, -s, 0.0, c)


@given(angle_strategy)
def test_mat3_rotation_z(angle: float):
    matrix = Mat3.rotation_z(angle)
    c = math.cos(angle)
    s = math.sin(angle)

    assert matrix == Mat3(c, -s, 0.0, s, c, 0.0, 0.0, 0.0, 1.0)


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_mat3_mul_vector(m00, m01, m02, m10, m11, m12, m20, m21, m22, x, y, z):
    matrix = Mat3(m00, m01, m02, m10, m11, m12, m20, m21, m22)
    vector = Vec3(x, y, z)

    assert matrix @ vector == Vec3(
        m00 * x + m01 * y + m02 * z,
        m10 * x + m11 * y + m12 * z,
        m20 * x + m21 * y + m22 * z,
    )


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_mat3_mul_matrix(a00, a01, a02, a10, a11, a12, a20, a21, a22, b00, b01, b02, b10, b11, b12, b20, b21, b22):
    matrix = Mat3(a00, a01, a02, a10, a11, a12, a20, a21, a22)
    other = Mat3(b00, b01, b02, b10, b11, b12, b20, b21, b22)

    expected = Mat3(
        a00 * b00 + a01 * b10 + a02 * b20,
        a00 * b01 + a01 * b11 + a02 * b21,
        a00 * b02 + a01 * b12 + a02 * b22,
        a10 * b00 + a11 * b10 + a12 * b20,
        a10 * b01 + a11 * b11 + a12 * b21,
        a10 * b02 + a11 * b12 + a12 * b22,
        a20 * b00 + a21 * b10 + a22 * b20,
        a20 * b01 + a21 * b11 + a22 * b21,
        a20 * b02 + a21 * b12 + a22 * b22,
    )

    assert matrix @ other == expected


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_mat3_transpose(m00, m01, m02, m10, m11, m12, m20, m21, m22):
    matrix = Mat3(m00, m01, m02, m10, m11, m12, m20, m21, m22)

    assert matrix.transpose() == Mat3(
        m00, m10, m20,
        m01, m11, m21,
        m02, m12, m22,
    )


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_mat3_transpose_twice(m00, m01, m02, m10, m11, m12, m20, m21, m22):
    matrix = Mat3(m00, m01, m02, m10, m11, m12, m20, m21, m22)

    assert matrix.transpose().transpose() == matrix


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_mat3_determinant(m00, m01, m02, m10, m11, m12, m20, m21, m22):
    matrix = Mat3(m00, m01, m02, m10, m11, m12, m20, m21, m22)

    expected = (
        m00 * (m11 * m22 - m12 * m21)
        - m01 * (m10 * m22 - m12 * m20)
        + m02 * (m10 * m21 - m11 * m20)
    )

    assert matrix.determinant() == expected


@given(integer_strategy, integer_strategy, integer_strategy, integer_strategy, integer_strategy, integer_strategy, integer_strategy, integer_strategy, integer_strategy)
def test_mat3_inverse(m00, m01, m02, m10, m11, m12, m20, m21, m22):
    matrix = Mat3(m00, m01, m02, m10, m11, m12, m20, m21, m22)
    determinant = matrix.determinant()

    if determinant == 0:
        with pytest.raises(ValueError):
            matrix.inverse()
        return

    inverse = matrix.inverse()

    assert_mat3_close(matrix @ inverse, Mat3.identity())
    assert_mat3_close(inverse @ matrix, Mat3.identity())


@given(float_strategy, float_strategy, float_strategy)
def test_mat3_transform_direction(x: float, y: float, z: float):
    matrix = Mat3.identity()
    direction = Vec3(x, y, z)

    assert matrix.transform_direction(direction) == direction


def test_mat3_normal_matrix_identity():
    matrix = Mat3.identity()

    assert_mat3_close(matrix.normal_matrix(), Mat3.identity())


@given(angle_strategy)
def test_mat3_rotation_x_preserves_length(angle: float):
    matrix = Mat3.rotation_x(angle)
    vector = Vec3(1.0, 2.0, 3.0)

    assert math.isclose((matrix @ vector).length(), vector.length(), rel_tol=1e-9, abs_tol=1e-9)


@given(angle_strategy)
def test_mat3_rotation_y_preserves_length(angle: float):
    matrix = Mat3.rotation_y(angle)
    vector = Vec3(1.0, 2.0, 3.0)

    assert math.isclose((matrix @ vector).length(), vector.length(), rel_tol=1e-9, abs_tol=1e-9)


@given(angle_strategy)
def test_mat3_rotation_z_preserves_length(angle: float):
    matrix = Mat3.rotation_z(angle)
    vector = Vec3(1.0, 2.0, 3.0)

    assert math.isclose((matrix @ vector).length(), vector.length(), rel_tol=1e-9, abs_tol=1e-9)