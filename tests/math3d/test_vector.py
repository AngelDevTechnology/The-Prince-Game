from engine.math3d.vector import Vec3


def test_add():
    a = Vec3(1, 2, 4)
    b = Vec3(7, 2, 3)

    assert a + b == Vec3(8, 4, 7)