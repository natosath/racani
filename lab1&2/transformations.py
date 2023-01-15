import numpy as np
from structures import Vertex
from math import sqrt
from pyglet.gl import *


# rotira z os za kut alpha
def z_rotacija(g1):
    sin_alpha = g1.y / (sqrt(g1.x ** 2 + g1.y ** 2))
    cos_alpha = g1.x / (sqrt(g1.x ** 2 + g1.y ** 2))
    G2 = Vertex(float((sqrt(g1.x ** 2 + g1.y ** 2))),
                float(0),
                float(g1.z))
    T2 = np.array([[cos_alpha, -sin_alpha, 0, 0],
                   [sin_alpha, cos_alpha, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    return G2, T2


# rotira y os za kut beta
def y_rotacija(g2):
    sin_beta = g2.x / (sqrt(g2.x ** 2 + g2.z ** 2))
    cos_beta = g2.z / (sqrt(g2.x ** 2 + g2.z ** 2))
    T3 = np.array([[cos_beta, 0, sin_beta, 0],
                   [0, 1, 0, 0],
                   [-sin_beta, 0, cos_beta, 0],
                   [0, 0, 0, 1]])
    return T3


def trans_pogleda(o, g):
    T1 = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 0, 1],
                   [-o.x, -o.y, - o.z, 1]])
    G1 = Vertex(float(g.x - o.x),
                float(g.y - o.y),
                float(g.z - o.z))
    G2, T2 = z_rotacija(G1)
    T3 = y_rotacija(G2)
    T4 = np.array([[0, -1, 0, 0],
                   [1, 0, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    T5 = np.array([[-1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    T25 = T2 @ T3 @ T4 @ T5
    Tuk = T1 @ T25
    # transpozirana zbog nacina na koji
    # OpenGL ucita tocke u glLoadMatrix
    return np.transpose(Tuk)


def perspektivna_projekcija(o, g):
    H = sqrt((o.x - g.x) ** 2 +
             (o.y - g.y) ** 2 +
             (o.z - g.z) ** 2)
    P = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, (1 / H)],
                  [0, 0, 0, 0]])
    return P


def cast_to_gl(array):
    normal_floats = []
    array = array.tolist()
    for row in array:
        for elem in row:
            normal_floats.append(elem)
    # vertices_gl_array = (GLfloat * len(vertices))(*vertices)
    # https://pyglet.readthedocs.io/en/latest/programming_guide/gl.html
    gl_floats = (GLfloat * len(normal_floats))(*normal_floats)
    return gl_floats


def transform_scene(ociste, glediste):
    T = trans_pogleda(ociste, glediste)
    P = perspektivna_projekcija(ociste, glediste)
    Transform_gl = cast_to_gl(T @ P)  # @ == matmul
    glLoadMatrixf(Transform_gl)
