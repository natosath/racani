from time import sleep

import numpy as np
from pyglet.gl import *
# from pyglet.gl.gl_compat import *

from bspline import create_curve_points, create_curve_tangents
from loader import load_obj_info, load_control_points_as_matrix
from render import render_obj, render_curve, render_tangent
from rotation import get_rotation_params
from structures import Vertex

window = pyglet.window.Window(height=720, width=1080, resizable=True)
# SCALING_FACTOR = window.height * 0.07
SCALING_FACTOR = 55

model_path = "obj/cube.obj"
ctrl_points_path = "inputs/lab1_single_curve.txt"
spiral_path = "inputs/lab1_spiral.txt"

# Load data
vertices, polygons, boundary, centre = load_obj_info(model_path)
spiral_points = load_control_points_as_matrix(spiral_path)

# Init
rotation_array = np.array([0, 0, 0])
translation = np.array([0, 0, 0])
trail = []
curve_point = None
glediste = Vertex(centre.x, centre.y, centre.z)
tangent_vector = None
rot_degree = 0
start_vector = np.array([0, 1, 1])  # 90 degrees


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(window.width / 5, window.height / 5, 0)
    # glTranslatef(-centre.x, -centre.y, -centre.z)

    glScalef(SCALING_FACTOR, SCALING_FACTOR, 0)

    # draw curve, has to go before translation
    render_curve(trail)

    glTranslatef(*translation)

    # draw tangent originating from object
    glColor3f(0, 1, 1)  # cyan
    render_tangent(tangent_vector)
    glColor3f(1, 1, 1)  # reset color

    # starting orientation and axes
    glRotatef(90, *start_vector)

    # new orientation
    glRotatef(rot_degree, *rotation_array)

    render_obj(vertices, polygons)
    # glOrtho(0, window.width, 0, window.height, -1, 1)


# init the scene
glMatrixMode(GL_MODELVIEW)

# animation
for i in range(0, len(spiral_points) - 3):
    print("Curve points:")
    print(spiral_points[i], spiral_points[i + 1], spiral_points[i + 2], spiral_points[i + 3], )
    R = np.array([spiral_points[i],
                  spiral_points[i + 1],
                  spiral_points[i + 2],
                  spiral_points[i + 3], ])
    curve = create_curve_points(R)
    tangents = create_curve_tangents(R)

    for curve_point, tangent in zip(curve, tangents):
        pyglet.clock.tick(poll=True)
        for window in pyglet.app.windows:

            rot_degree, rotation_array = get_rotation_params(start_vector, tangent)
            tangent_vector = tangent

            translation = curve_point
            trail.append(translation)

            if len(trail) > 300:
                trail = trail[1:]

            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()
        sleep(0.005)
# pyglet.app.run()
