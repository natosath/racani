import numpy as np
from loader import load_control_points_as_matrix

Bi3 = (1 / 6) * np.array([[-1, 3, -3, 1],
                          [3, -6, 3, 0],
                          [-3, 0, 3, 0],
                          [1, 4, 1, 0], ])

Bi_tangent = (1 / 2) * np.array([[-1, 3, -3, 1],
                                 [2, -4, 2, 0],
                                 [-1, 0, 1, 0], ])


def create_curve_points(Ri, steps=100):
    bspline_curve = []
    for i in range(0, steps + 1):
        t = i / steps
        T = np.array([t ** 3, t ** 2, t, 1])
        pt = T @ Bi3 @ Ri
        bspline_curve.append(pt)
    return bspline_curve


def create_curve_tangents(Ri, steps=100):
    tangents = []
    for i in range(0, steps + 1):
        t = i / steps
        T = np.array([t ** 2, t, 1])
        tan = T @ Bi_tangent @ Ri
        tangents.append(tan)
    return tangents


if __name__ == "__main__":
    R = load_control_points_as_matrix("inputs/lab1_single_curve.txt")
    curve = create_curve_points(R)
    for p in curve:
        print(p)
    curve_tangents = create_curve_tangents(R)
    print(curve_tangents)
