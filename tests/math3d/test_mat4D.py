import math

import pytest
from hypothesis import given, strategies as st

from engine.math3d.mat4D import Mat4
from engine.math3d.vector3D import Vec3
from engine.math3d.vector4D import Vec4


float_strategy = st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)

integer_strategy = st.integers(min_value=-5, max_value=5)

angle_strategy = st.floats(min_value=-2 * math.pi, max_value=2 * math.pi, allow_nan=False, allow_infinity=False)


def assert_mat4_close(actual: Mat4, expected: Mat4):
    assert math.isclose(actual.m00, expected.m00, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m01, expected.m01, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m02, expected.m02, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m03, expected.m03, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m10, expected.m10, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m11, expected.m11, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m12, expected.m12, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m13, expected.m13, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m20, expected.m20, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m21, expected.m21, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m22, expected.m22, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m23, expected.m23, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m30, expected.m30, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m31, expected.m31, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m32, expected.m32, rel_tol=1e-9, abs_tol=1e-9)
    assert math.isclose(actual.m33, expected.m33, rel_tol=1e-9, abs_tol=1e-9)


def test_mat4_identity():
    assert Mat4.identity() == Mat4(
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )


@given(float_strategy, float_strategy, float_strategy, float_strategy)
def test_mat4_identity_transform(x: float, y: float, z: float, w: float):
    matrix = Mat4.identity()
    vector = Vec4(x, y, z, w)

    assert matrix @ vector == vector


@given(float_strategy, float_strategy, float_strategy)
def test_mat4_translation(x: float, y: float, z: float):
    position = Vec3(x, y, z)
    matrix = Mat4.translation(position)

    assert matrix == Mat4(
        1.0, 0.0, 0.0, x,
        0.0, 1.0, 0.0, y,
        0.0, 0.0, 1.0, z,
        0.0, 0.0, 0.0, 1.0,
    )


@given(float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy, float_strategy)
def test_mat4_scale(sx: float, sy: float, sz: float, x: float, y: float, z: float, w: float):
    scale = Vec3(sx, sy, sz)
    matrix = Mat4.scale(scale)
    vector = Vec4(x, y, z, w)

    assert matrix @ vector == Vec4(sx * x, sy * y, sz * z, w)


@given(angle_strategy)
def test_mat4_rotation_x(angle: float):
    matrix = Mat4.rotation_x(angle)
    c = math.cos(angle)
    s = math.sin(angle)

    assert matrix == Mat4(
        1.0, 0.0, 0.0, 0.0,
        0.0, c, -s, 0.0,
        0.0, s, c, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )


@given(angle_strategy)
def test_mat4_rotation_y(angle: float):
    matrix = Mat4.rotation_y(angle)
    c = math.cos(angle)
    s = math.sin(angle)

    assert matrix == Mat4(
        c, 0.0, s, 0.0,
        0.0, 1.0, 0.0, 0.0,
        -s, 0.0, c, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )


@given(angle_strategy)
def test_mat4_rotation_z(angle: float):
    matrix = Mat4.rotation_z(angle)
    c = math.cos(angle)
    s = math.sin(angle)

    assert matrix == Mat4(
        c, -s, 0.0, 0.0,
        s, c, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )


@given(
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
)
def test_mat4_mul_vector(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33, x, y, z, w):
    matrix = Mat4(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33)
    vector = Vec4(x, y, z, w)

    assert matrix @ vector == Vec4(
        m00 * x + m01 * y + m02 * z + m03 * w,
        m10 * x + m11 * y + m12 * z + m13 * w,
        m20 * x + m21 * y + m22 * z + m23 * w,
        m30 * x + m31 * y + m32 * z + m33 * w,
    )


@given(
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
)
def test_mat4_mul_matrix(
    a00, a01, a02, a03, a10, a11, a12, a13, a20, a21, a22, a23, a30, a31, a32, a33,
    b00, b01, b02, b03, b10, b11, b12, b13, b20, b21, b22, b23, b30, b31, b32, b33,
):
    matrix = Mat4(a00, a01, a02, a03, a10, a11, a12, a13, a20, a21, a22, a23, a30, a31, a32, a33)
    other = Mat4(b00, b01, b02, b03, b10, b11, b12, b13, b20, b21, b22, b23, b30, b31, b32, b33)

    expected = Mat4(
        a00 * b00 + a01 * b10 + a02 * b20 + a03 * b30,
        a00 * b01 + a01 * b11 + a02 * b21 + a03 * b31,
        a00 * b02 + a01 * b12 + a02 * b22 + a03 * b32,
        a00 * b03 + a01 * b13 + a02 * b23 + a03 * b33,
        a10 * b00 + a11 * b10 + a12 * b20 + a13 * b30,
        a10 * b01 + a11 * b11 + a12 * b21 + a13 * b31,
        a10 * b02 + a11 * b12 + a12 * b22 + a13 * b32,
        a10 * b03 + a11 * b13 + a12 * b23 + a13 * b33,
        a20 * b00 + a21 * b10 + a22 * b20 + a23 * b30,
        a20 * b01 + a21 * b11 + a22 * b21 + a23 * b31,
        a20 * b02 + a21 * b12 + a22 * b22 + a23 * b32,
        a20 * b03 + a21 * b13 + a22 * b23 + a23 * b33,
        a30 * b00 + a31 * b10 + a32 * b20 + a33 * b30,
        a30 * b01 + a31 * b11 + a32 * b21 + a33 * b31,
        a30 * b02 + a31 * b12 + a32 * b22 + a33 * b32,
        a30 * b03 + a31 * b13 + a32 * b23 + a33 * b33,
    )

    assert matrix @ other == expected


@given(
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
)
def test_mat4_transpose(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33):
    matrix = Mat4(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33)

    assert matrix.transpose() == Mat4(
        m00, m10, m20, m30,
        m01, m11, m21, m31,
        m02, m12, m22, m32,
        m03, m13, m23, m33,
    )


@given(
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
    float_strategy, float_strategy, float_strategy, float_strategy,
)
def test_mat4_transpose_twice(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33):
    matrix = Mat4(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33)

    assert matrix.transpose().transpose() == matrix


@given(
    integer_strategy, integer_strategy, integer_strategy, integer_strategy,
    integer_strategy, integer_strategy, integer_strategy, integer_strategy,
    integer_strategy, integer_strategy, integer_strategy, integer_strategy,
    integer_strategy, integer_strategy, integer_strategy, integer_strategy,
)
def test_mat4_inverse(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33):
    matrix = Mat4(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33)

    try:
        inverse = matrix.inverse()
    except ValueError:
        with pytest.raises(ValueError):
            matrix.inverse()
        return

    assert_mat4_close(matrix @ inverse, Mat4.identity())
    assert_mat4_close(inverse @ matrix, Mat4.identity())


@given(angle_strategy)
def test_mat4_rotation_x_preserves_length(angle: float):
    matrix = Mat4.rotation_x(angle)
    vector = Vec4(1.0, 2.0, 3.0, 1.0)

    result = matrix @ vector

    assert math.isclose(
        math.hypot(result.x, result.y, result.z),
        math.hypot(vector.x, vector.y, vector.z),
        rel_tol=1e-9,
        abs_tol=1e-9,
    )


@given(angle_strategy)
def test_mat4_rotation_y_preserves_length(angle: float):
    matrix = Mat4.rotation_y(angle)
    vector = Vec4(1.0, 2.0, 3.0, 1.0)

    result = matrix @ vector

    assert math.isclose(
        math.hypot(result.x, result.y, result.z),
        math.hypot(vector.x, vector.y, vector.z),
        rel_tol=1e-9,
        abs_tol=1e-9,
    )


@given(angle_strategy)
def test_mat4_rotation_z_preserves_length(angle: float):
    matrix = Mat4.rotation_z(angle)
    vector = Vec4(1.0, 2.0, 3.0, 1.0)

    result = matrix @ vector

    assert math.isclose(
        math.hypot(result.x, result.y, result.z),
        math.hypot(vector.x, vector.y, vector.z),
        rel_tol=1e-9,
        abs_tol=1e-9,
    )


def test_mat4_perspective_invalid_aspect():
    with pytest.raises(ValueError):
        Mat4.perspective(math.pi / 2, 0.0, 0.1, 100.0)


def test_mat4_perspective_invalid_near_far():
    with pytest.raises(ValueError):
        Mat4.perspective(math.pi / 2, 1.0, 100.0, 0.1)


def test_mat4_perspective_invalid_fov():
    with pytest.raises(ValueError):
        Mat4.perspective(0.0, 1.0, 0.1, 100.0)


@given(
    st.floats(min_value=0.1, max_value=3.0, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0.1, max_value=3.0, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0.01, max_value=10.0, allow_nan=False, allow_infinity=False),
    st.floats(min_value=10.01, max_value=1000.0, allow_nan=False, allow_infinity=False),
)
def test_mat4_perspective(fov: float, aspect: float, near: float, far: float):
    matrix = Mat4.perspective(fov, aspect, near, far)

    f = 1.0 / math.tan(fov * 0.5)

    expected = Mat4(
        f / aspect, 0.0, 0.0, 0.0,
        0.0, f, 0.0, 0.0,
        0.0, 0.0, (far + near) / (near - far), (2.0 * far * near) / (near - far),
        0.0, 0.0, -1.0, 0.0,
    )

    assert_mat4_close(matrix, expected)


def test_mat4_orthographic_invalid_left_right():
    with pytest.raises(ValueError):
        Mat4.orthographic(1.0, 1.0, -1.0, 1.0, 0.1, 100.0)


def test_mat4_orthographic_invalid_bottom_top():
    with pytest.raises(ValueError):
        Mat4.orthographic(-1.0, 1.0, 1.0, 1.0, 0.1, 100.0)


def test_mat4_orthographic_invalid_near_far():
    with pytest.raises(ValueError):
        Mat4.orthographic(-1.0, 1.0, -1.0, 1.0, 1.0, 1.0)


@given(
    st.floats(min_value=-10.0, max_value=-0.1, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False),
    st.floats(min_value=-10.0, max_value=-0.1, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False),
    st.floats(min_value=-10.0, max_value=-0.1, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False),
)
def test_mat4_orthographic(left: float, right: float, bottom: float, top: float, near: float, far: float):
    matrix = Mat4.orthographic(left, right, bottom, top, near, far)

    expected = Mat4(
        2.0 / (right - left), 0.0, 0.0, -(right + left) / (right - left),
        0.0, 2.0 / (top - bottom), 0.0, -(top + bottom) / (top - bottom),
        0.0, 0.0, -2.0 / (far - near), -(far + near) / (far - near),
        0.0, 0.0, 0.0, 1.0,
    )

    assert_mat4_close(matrix, expected)