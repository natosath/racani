import pyglet
from pyglet.gl import *
import numpy as np

from structures import Vertex


def render_obj(vertices, polygons, verbose=False):
    if verbose: print("rendering...", end="")
    for poly in polygons:
        first = vertices[poly.v1]
        second = vertices[poly.v2]
        third = vertices[poly.v3]

        glBegin(GL_LINE_LOOP)
        glVertex3f(first.x, first.y, first.z)
        glVertex3f(second.x, second.y, second.z)
        glVertex3f(third.x, third.y, third.z)
        glEnd()
    if verbose: print("...done")


# renders object in interval [0,2]
def render_obj_shifted(vertices, polygons, boundary, verbose=False):
    if verbose: print("rendering...", end="")
    for poly in polygons:
        first = vertices[poly.v1]
        second = vertices[poly.v2]
        third = vertices[poly.v3]
        # normalize from [-1,1] to [0, 2]
        glBegin(GL_LINE_LOOP)
        glVertex3f(first.x + abs(boundary.x_min), first.y + abs(boundary.y_min), first.z + abs(boundary.z_min))
        glVertex3f(second.x + abs(boundary.x_min), second.y + abs(boundary.y_min), second.z + abs(boundary.z_min))
        glVertex3f(third.x + abs(boundary.x_min), third.y + abs(boundary.y_min), third.z + abs(boundary.z_min))
        glEnd()
    if verbose: print("...done")


def front_polygon(vertex, polygon):
    product = (polygon.a * vertex.x + polygon.b * vertex.y +
               polygon.c * vertex.z + polygon.d)
    if product >= 0:
        return True
    return False


def render_curve(trail):
    glBegin(GL_LINE_STRIP)
    for v in trail:
        glVertex3f(*v)
    glEnd(GL_LINE_STRIP)


def render_tangent(tangent):
    glBegin(GL_LINE_STRIP)
    for i in range(-25, 25):
        scale = i / 100
        scaled = scale * tangent
        glVertex3f(*scaled)
    glEnd(GL_LINE_STRIP)


def render_particle(particle, size=50):
    c = particle.color
    p = particle.vertex
    glColor4f(c.r, c.g, c.b, c.alpha)
    # glBindTexture(GL_TEXTURE_2D_ARRAY, particle.texture)

    glPushMatrix()
    glTranslatef(p.x, p.z, p.y)
    glRotatef(particle.angle, *particle.rotation)

    glBegin(GL_QUADS)
    glTexCoord2d(0.0, 0.0)
    glVertex3f(-size, -size, 0.0)
    glTexCoord2d(1.0, 0.0)
    glVertex3f(-size, size, 0.0)
    glTexCoord2d(1.0, 1.0)
    glVertex3f(size, size, 0.0)
    glTexCoord2d(0.0, 1.0)
    glVertex3f(size, -size, 0.0)
    glEnd()

    glPopMatrix()


def render_particles(particles, size=50):
    for p in particles:
        render_particle(p, size)
