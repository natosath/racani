import numpy as np

from structures import Vertex, Polygon, ObjBoundary


def load_obj_info(path):
    vertices = []  # vertices have to be in order
    polygons = set()  # polygons don't have to be, set for better performance
    x_vertex = set()
    y_vertex = set()
    z_vertex = set()
    with open(path) as file:
        data = file.readlines()
    for line in data:
        if line[0] == "v":
            line = line[1:].strip().split()
            x_vertex.add(float(line[0]))
            y_vertex.add(float(line[1]))
            z_vertex.add(float(line[2]))
            vertices.append(Vertex(float(line[0]),
                                   float(line[1]),
                                   float(line[2])))
        elif line[0] == "f":
            line = line[1:].strip().split()
            # -1 cuz it starts from 1, not 0
            polygons.add(Polygon(int(line[0]) - 1,
                                 int(line[1]) - 1,
                                 int(line[2]) - 1))
    boundary = ObjBoundary(min(x_vertex), max(x_vertex),
                           min(y_vertex), max(y_vertex),
                           min(z_vertex), max(z_vertex))
    arith_mean_centre = Vertex((boundary.x_max + boundary.x_min) * 0.5,
                               (boundary.y_max + boundary.y_min) * 0.5,
                               (boundary.z_max + boundary.z_min) * 0.5)

    return vertices, polygons, boundary, arith_mean_centre


def load_control_vertex(path):
    control_points = []
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            control_points.append(Vertex.from_str(line.strip()))
    return control_points


def load_control_points_as_matrix(path):
    control_points = []
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            control_points.append(list(map(float, str(line).strip().split())))

    return np.array(control_points)
