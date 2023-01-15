import random
import numpy as np
from dataclasses import dataclass
from rotation import get_rotation_params
import math

VELOCITY = 8

def rotation_wrapper(vertex, ociste):
    rot_degree, rotation_array = get_rotation_params(np.array([0, 0, 1]),
                                                     np.array([vertex.x - ociste.x,
                                                               vertex.y - ociste.y,
                                                               vertex.z - ociste.z, ]))
    return math.degrees(rot_degree), rotation_array


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.z)

    @classmethod
    def from_str(cls, line):
        x, y, z = map(float, str(line).strip().split())
        return cls(x, y, z)

    @classmethod
    def from_np(cls, array):
        x, y, z = array[0], array[1], array[2],
        return cls(x, y, z)


class ObjBoundary:
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max


class Polygon:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def __str__(self):
        return str(self.v1) + "," + str(self.v2) + "," + str(self.v3)


@dataclass
class Color:
    r: float
    g: float
    b: float
    alpha: float


class Particle:
    def __init__(self, vertex, color, vector, angle, rotation, texture):
        self.vertex = vertex
        self.color = color
        self.vector = vector
        self.angle = angle
        self.rotation = rotation
        self.texture = texture

    def translate(self):
        self.vertex = Vertex(self.vertex.x + self.vector.x,
                             self.vertex.y + self.vector.y,
                             self.vertex.z + self.vector.z, )

    def recolor(self):  # 0.99
        self.color = Color(self.color.r * 0.9,
                           self.color.g * 0.9,
                           self.color.b * 0.9,
                           self.color.alpha * 0.9, )

    def reorient(self, ociste):
        self.angle, self.rotation = rotation_wrapper(self.vertex, ociste)


@dataclass
class ParticleSpawner:
    x: int
    y: int
    z: int
    texture: ...
    vertex: Vertex = Vertex(0, 0, 0)

    def position(self) -> Vertex:
        self.vertex = Vertex(self.x + random.uniform(-0.1, 0.1),
                             self.y + random.uniform(-0.1, 0.1),
                             0, )
        return self.vertex

    def color(self) -> Color:
        return Color(0.6 + random.uniform(-0.4, 0.4),
                     0.6 + random.uniform(-0.4, 0.4),
                     0.6 + random.uniform(-0.4, 0.4),
                     0.9 + random.uniform(-0.1, 0.1), )

    def translation(self) -> Vertex:
        return Vertex(random.uniform(-VELOCITY, VELOCITY),
                      random.uniform(-VELOCITY, VELOCITY),
                      random.uniform(-VELOCITY, VELOCITY), )

    def rotation(self, ociste) -> (float, np.array):
        # return 0, np.array([0, 0, 5])
        return rotation_wrapper(self.vertex, ociste)

    def spawn(self, ociste):
        self.position()
        angle, rotation_vector = self.rotation(ociste)
        return Particle(self.vertex, self.color(), self.translation(),
                        angle, rotation_vector, self.texture)
