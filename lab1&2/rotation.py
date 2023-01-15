import math

import numpy as np


def get_rotation_params(start, end):
    rotation_array = np.cross(start, end)
    rot_cos = np.dot(start, end) / (np.linalg.norm(start) * (np.linalg.norm(end)))
    rot_degree = np.arccos(rot_cos) * 180 / math.pi

    return rot_degree, rotation_array
