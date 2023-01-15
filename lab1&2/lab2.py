from time import sleep

import numpy as np
from OpenGL.raw.GLUT import *
from pyglet.gl import *
from pyglet import image
from structures import Vertex, ParticleSpawner
from pyglet.window import key
from render import render_particles
from transformations import transform_scene

height, width = 720, 1080
window = pyglet.window.Window(height=height, width=width, resizable=True)
SCALING_FACTOR = 0.006
SIZE = 2
SPAWN_RATE = 5

# Init
rotation_array = np.array([0, 0, 0])
translation = np.array([0, 0, 0])
particles = []

img = image.load("particle/explosion.bmp")
texture = img.get_texture()
ociste = Vertex(1, 1, 5)
glediste = Vertex(0, 0, 0)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # glOrtho(0, window.width, 0, window.height, -100, 100)
    # glTranslatef(height / 2, width / 2, 0)
    transform_scene(ociste, glediste)
    glScalef(SCALING_FACTOR, SCALING_FACTOR, SCALING_FACTOR)
    render_particles(particles, size=SIZE)
    # glTranslatef(-height / 2, -width / 2, 0)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        ociste.x -= 1
    if symbol == key.D:
        ociste.x += 1
    if symbol == key.R:
        ociste.x = 0
    if symbol == key.ESCAPE:
        exit()


# init the scene
glEnable(texture.target)  # typically target is GL_TEXTURE_2D
glBindTexture(texture.target, texture.id)

# pyglet.app.run()

# animation
spawner = ParticleSpawner(0, 0, 0, texture)
while True:
    for i in range(SPAWN_RATE):
        particles.append(spawner.spawn(ociste))

    remaining_particles = []
    for p in particles:
        p.translate()
        p.recolor()
        p.reorient(ociste)
        if p.color.alpha > 0.1:
            remaining_particles.append(p)
    particles = remaining_particles

    window.switch_to()
    window.dispatch_events()
    window.dispatch_event('on_draw')
    window.flip()
    sleep(0.1)
