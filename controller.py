"""
Contralor de la aplicación.
"""

import glfw
import sys


class Controller(object):

    def __init__(self):
        self.fill_polygon = True
        self.toggle = {}
        self.leftClickOn = False
        self.theta = 0.0
        self.mousePos = (0.0, 0.0)

    def set_toggle(self, tp, key):
        self.toggle[key] = tp

    def on_key(self, window, key, scancode, action, mods):
        plane = self.toggle['plane']
        controls = self.toggle['controls']
        """
        if action != glfw.PRESS:
            return
        """

        if key == glfw.KEY_SPACE:
            self.fill_polygon = not self.fill_polygon

        elif key == glfw.KEY_F:
            self.toggle['face'].toggle()

        elif key == glfw.KEY_Q:
            self.toggle['axis'].toggle()
        
        elif key == glfw.KEY_ESCAPE:
            sys.exit()

        elif key == glfw.KEY_W:
            plane.accelerate()       
            plane.accelerateRPM(controls.revolutions.getAngle())

        elif key == glfw.KEY_S:
            plane.decelerate()
        
        elif key == glfw.KEY_UP:
            plane.headUp()

        elif key == glfw.KEY_DOWN:
            plane.headDown()

        else:
            print('Unknown key')
        
    def cursor_pos_callback(self,window, x, y):
        self.mousePos = (x,y)


    def mouse_button_callback(self,window, button, action, mods):
        plane = self.toggle['plane']
        controls = self.toggle['controls']
        velocimeter = controls.velocimeter
        pitching = controls.pitching
        revolutions = controls.revolutions
        height = controls.height
        """
        glfw.MOUSE_BUTTON_1: left click
        glfw.MOUSE_BUTTON_2: right click
        glfw.MOUSE_BUTTON_3: scroll click
        """

        if (action == glfw.PRESS or action == glfw.REPEAT):
        
            (x,y) = (glfw.get_cursor_pos(window))
            
            if 510 <= x <= 536 and 512 <= y <= 532:
                controls.changeState("motor",plane, [velocimeter,revolutions, height, pitching])
                
            elif 510 <= x <= 538 and 540 <= y <= 560:
                controls.changeState("gassoline", plane, [velocimeter,revolutions, height, pitching])
            
            elif 510 <= x <= 538 and 569 <= y <= 589:
                controls.changeState("panelButton",plane, [velocimeter,revolutions, height, pitching])
                
        elif (action ==glfw.RELEASE):
            if (button == glfw.MOUSE_BUTTON_1):
                self.leftClickOn = False


    def scroll_callback(window, x, y):

        print("Mouse scroll:", x, y)
    
