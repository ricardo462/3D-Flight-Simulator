"""
Visualizador.
"""

import glfw
from OpenGL.GL import *
import numpy as np
import sys
import random

import transformations2 as tr2
import easy_shaders as es

from model import *
from controller import Controller


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600 
    window = glfw.create_window(width, height, 'Epic Flight Simulator 3D', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Creamos el controlador
    controller = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)
    glfw.set_cursor_pos_callback(window, controller.cursor_pos_callback)
    glfw.set_mouse_button_callback(window, controller.mouse_button_callback)
    glfw.set_scroll_callback(window, controller.scroll_callback)
    # Creating shader programs for textures and for colores
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    

    # Setting up the clear screen color
    glClearColor(1,1,1,1)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creamos los objetos
    
    axis = Axis() 
    plane = Plane() 
    floor = Floor()
    river = River()
    controls = Controls()
    clouds = Clouds()
    explosion = Explosion()

    mountains = Mountains()
    day = True
    mountains.create(day)
    clouds.create()

    controller.set_toggle(axis, 'axis')
    controller.set_toggle(plane, 'plane')
    controller.set_toggle(controls,'controls')
    

    
    # Creamos la camara y la proyección
    projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)
    view = tr2.lookAt(
        np.array([10, 10, 5]),  # Donde está parada la cámara
        np.array([0, 0, 0]),  # Donde estoy mirando
        np.array([0, 0, 1])  # Cual es vector UP
    )

    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()
        # Filling or not the shapes depending on the controller state
        if controller.fill_polygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



        glUseProgram(colorShaderProgram.shaderProgram)

        # Dibujamos
        
        #axis.draw(colorShaderProgram, projection, view)
    
        plane.update()
        plane.friction()
        plane.draw(colorShaderProgram, projection, view)

        mountains.delete()
        clouds.delete()
        number = random.random()
        if number < 0.001/2:
            day = not day
        mountains.create(day)
        clouds.create()
        inertia = 0
        if plane.getVelocity() >100:
            inertia = 0.0001
        
        plane.decelerateRPM(controls.revolutions.getAngle())
        mountains.update(plane.getVelocity()*(0.0001*np.cos(plane.angle)+inertia))
        mountains.draw(colorShaderProgram, projection, view)
        clouds.update(0.5*plane.getVelocity()*(0.0001*np.cos(plane.angle)+inertia))
        clouds.draw(colorShaderProgram, projection, view)

        floor.draw(colorShaderProgram, projection, view)

        river.draw(colorShaderProgram, projection, view)
        controls.draw(colorShaderProgram,projection, view)
        controls.update(plane.getVelocity(),plane.getRPM(),plane.getHeight(),plane.getAngle())
        
        plane.explode(explosion)
        explosion.update(0,plane.getHeight())
        explosion.draw(colorShaderProgram)
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
