"""
Hacemos los modelos
"""
import numpy as np
import scene_graph2 as sg
import basic_shapes as bs
import transformations2 as tr
import easy_shaders as es
import random

from OpenGL.GL import *

class Pyramid:
    def __init__(self,r,g,b):
        gpuPyramid = es.toGPUShape(bs.createPyramid(r,g,b))
        pyramid = sg.SceneGraphNode("pyramid")
        pyramid.transform = tr.uniformScale(0.5)
        pyramid.childs += [gpuPyramid]
        self.model = pyramid

    def draw(self,pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

class Plane:
    def __init__(self):
        gpuWhitePyramid = es.toGPUShape(bs.createPyramid(0,0,0))
        gpuWhiteCube = es.toGPUShape(bs.createColorCube(0,0,1))
        gpuWhiteTriangularPrism = es.toGPUShape(bs.crateTriangularPrism(0,0,0))
        gpuBlackCube = es.toGPUShape(bs.createColorCube(0,0,0))

        wing = sg.SceneGraphNode("wing")
        wing.transform = tr.matmul([tr.scale(0.5,2,0.1),tr.translate(1,0.11,3)])
        wing.childs += [gpuBlackCube]


        triangularPrism = sg.SceneGraphNode("triangularPrism")
        triangularPrism.transform = tr.matmul([tr.rotationZ(np.pi), tr.translate(-1,-.5,0.5),tr.scale(1,1,0.4)])
        triangularPrism.childs = [gpuWhiteTriangularPrism]

        whitePyramid = sg.SceneGraphNode("pyramid")
        whitePyramid.transform = tr.rotationY(-np.pi/2)
        #whitePyramid.transform = tr.uniformScale(0)
        whitePyramid.childs += [gpuWhitePyramid]

        whiteBody = sg.SceneGraphNode("body")
        whiteBody.transform = tr.matmul([tr.scale(1,0.5,0.5),tr.translate(0.5,0.5,0.5)])
        #whiteBody.transform = tr.uniformScale(0)
        whiteBody.childs += [gpuWhiteCube]

        body = sg.SceneGraphNode("plane")
        #body.transform = tr.scale(0.5,0.5,0.2)
        body.transform = tr.matmul([tr.uniformScale(0.3),tr.translate(-0.3,0,0)])
        body.childs += [whiteBody,whitePyramid,triangularPrism,wing]
        
        self.model = body
        self.angle = 0.01 
        self.velocity = 0
        self.freeFall = False
        self.time = 0
        self.ground = True
        self.RPM = 0
        self.on = True
        self.explosion = False

    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)


    def headUp(self):
        if self.on:
            if self.ground:
                if self.getHeight() >= -0.435 and self.velocity>=50:
                    self.angle += 0.04
                    self.model.transform = tr.rotationY2(self.model.transform,self.angle)
            else:
                self.angle += 0.04
                self.model.transform = tr.rotationY2(self.model.transform,self.angle)
             
    def headDown(self):
        if self.on:
            if self.ground:
                if self.getHeight() >= -0.435 and self.velocity>=50:
                    self.angle += 0.04
                    self.model.transform = tr.rotationY2(self.model.transform,self.angle)
            else:
                self.angle -=0.04
                self.model.transform = tr.rotationY2(self.model.transform,self.angle)
    

        
    def accelerate(self):
        if self.on:
            if self.velocity <= 360:
                self.velocity +=0.5
                
    def accelerateRPM(self,angle):
        if self.on:
            if angle>-np.pi*1.7:
                self.RPM +=5   
        
    def decelerateRPM(self,angle):
        if angle<=0:
            self.RPM -=1
    
    def decelerate(self):
        if self.on:
            self.velocity -=0.2
        
    def friction(self):
        if self.velocity > 0:
            self.velocity -= 0.02
            if self.velocity > 340:
                self.velocity -= 5
        elif self.velocity <0:
            self.velocity += 0.02
        
        if self.getHeight()>0:
            if self.velocity >= 0:
                self.velocity -= np.sin(self.angle)*0.1
        
        # Gravity
        if self.angle <= 0:
            self.velocity += np.sin(-self.angle)*0.5

    def getVelocity(self):
        return self.velocity
    
    def getHeight(self):
        return self.model.transform[2,3]
    
    def getRPM(self):
        return self.RPM
    
    def getAngle(self):
        return self.angle
    
    def update(self):
        g = 9.8
        if not self.explosion:
            if self.getHeight()<= 0:
                self.ground = True
            else:
                self.ground = False
            if self.velocity >=50:
                self.freeFall = False
                self.model.transform = tr.translate2(self.model.transform,0,0,0.00005*np.sin(self.angle)*self.velocity)
            
            elif self.getHeight() > 0 and self.velocity < 50:
                if not self.freeFall:
                    self.time = 0
                self.freeFall = True
                dy = 0.5*g*self.time**2
                self.model.transform = tr.translate2(self.model.transform,0,0,-dy)
                self.time += 0.0001
           
        if self.explosion:
            if self.velocity >= 0:
                if self.velocity <= 2:
                    self.velocity = 0
                self.velocity -= 1
            if self.getHeight() >= -0.0:
                self.model.transform = tr.translate2(self.model.transform,0,0,-0.01)
            
    
    def explode(self, explosion):
        if self.getHeight() <= -0.1:
            explosion.explode(-0.7,self.getHeight())
            self.on = False
            self.explosion = True
            
        if self.velocity >= 320:
            num = random.random()
            if num*self.velocity >333: 
                explosion.explode(-0.7,self.getHeight())
                self.on = False
                self.explosion = True
        
class Mountain:

    def __init__(self,day):
        if day:
            (r,g,b) = (0,np.random.uniform(0.4,1,1),0)
        else:
            (r,g,b) = (np.random.uniform(0.2,0.7),np.random.uniform(0,0.3),0)
        
        y1 = np.random.uniform(-2,-0.8)
        y2 = np.random.uniform(0.8,2)
        num = np.random.uniform(0,1)
        if num < 0.5:
            y = y1
        else:
            y = y2
        gpuPyramid = es.toGPUShape(bs.createPyramid(r,g,b))
        
        mountain = sg.SceneGraphNode("mountain")
        mountain.transform = tr.translate2(mountain.transform,-3.5,y,0)
        
        mountain.childs += [gpuPyramid]
        self.model = mountain
        
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)
        
    def update(self,dt):
        self.model.transform = tr.translate2(self.model.transform,dt,0,0)

class Mountains:
    
    def __init__(self):
        self.mountains = np.array([])
        
        
    def draw(self, pipeline_color, projection, view):
        for k in self.mountains:
            k.draw(pipeline_color, projection, view)
    
    def create(self,day):
        if len(self.mountains) >=10:
            return
        num = np.random.random()
        if num <0.05:
            self.mountains = np.append(self.mountains, Mountain(day))
            
    def delete(self):
        remain_mountains = np.array([])
        for i in self.mountains:
            matrix = i.model.transform
            x = matrix[0,3]
            if x<1.6:
                remain_mountains = np.append(remain_mountains,i)
                
        self.mountains = remain_mountains

    def update(self, dt):
        for k in self.mountains:
            k.update(dt)
            
    def getMountains(self):
        return self.mountains
    
    def one(self):
        self.mountains = Mountain()
        
    def printM(self,pipeline):
        self.mountains.draw(pipeline)

class Cloud:

    def __init__(self):
        y1 = np.random.uniform(-2,-0.8)
        y2 = np.random.uniform(0.8,2)
        num = np.random.uniform(0,1)
        h = np.random.uniform(0.2,0.4)
        if num < 0.5:
            y = y1
        else:
            y = y2
        gpuCube = es.toGPUShape(bs.createColorCube(1,1,1))

        
        cloud = sg.SceneGraphNode("cloud")
        cloud.transform = tr.matmul([tr.translate2(cloud.transform,-2,y,h),tr.scale(0.5,0.2,0.1)])
        
        cloud.childs += [gpuCube]
        self.model = cloud
        
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)
        
    def update(self,dt):
        self.model.transform = tr.translate2(self.model.transform,dt,0,0)

class Clouds:
    
    def __init__(self):
        self.clouds = np.array([])
        
        
    def draw(self, pipeline_color, projection, view):
        for k in self.clouds:
            k.draw(pipeline_color, projection, view)
    
    def create(self):
        if len(self.clouds) >=7:
            return
        num = np.random.random()
        if num <0.05:
            self.clouds = np.append(self.clouds, Cloud())
            
    def delete(self):
        remain_clouds = np.array([])
        for i in self.clouds:
            matrix = i.model.transform
            x = matrix[0,3]
            if x<1.5:
                remain_clouds = np.append(remain_clouds,i)
                
        self.clouds = remain_clouds

    def update(self, dt):
        for k in self.clouds:
            k.update(dt)
            
    def getMountains(self):
        return self.mountains
    
    def one(self):
        self.mountains = Mountain()
        
    def printM(self,pipeline):
        self.mountains.draw(pipeline)



class Floor:
    def __init__(self):
        gpuGreenQuad = es.toGPUShape(bs.createColorQuad(194/255,155/255,97/255))

        floor = sg.SceneGraphNode("floor")
        floor.transform = tr.uniformScale(6)
        floor.childs += [gpuGreenQuad]

        self.model = floor
    
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

class River:
    def __init__(self):
        gpuLightBlueQuad = es.toGPUShape(bs.createColorQuad(0,170/255,228/255))

        river = sg.SceneGraphNode("river")
        river.transform = tr.matmul([tr.scale(6,0.4,1),tr.translate(0,0,0.001)])
        river.childs += [gpuLightBlueQuad]
        
        self.model = river

    
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

class Board:
    
    def __init__(self):
        gpuRectangle = es.toGPUShape(bs.createColorQuad(0, 0, 0))
        
        board = sg.SceneGraphNode("board")
        board.transform = tr.translate3(2, 0.5, 1, 0, -0.75, 0.001)
        board.childs += [gpuRectangle]
        self.model = board
        
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

        
        
        
class Circle:
    def __init__(self,x,y):
        
        gpuCircle = es.toGPUShape(bs.createColorCircle(40,0.9,0.9,0.9))
        circle = sg.SceneGraphNode("circle")
        circle.transform = tr.uniformScale(0.3)
        circle.transform = tr.translate2(circle.transform,x,y,0)
        circle.childs += [gpuCircle]
        self.model = circle
    
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

        
    
        
class CircleInstrument:
    def __init__(self,x,y,name,limits=[]):
        
        gpuBlackRectangle = es.toGPUShape(bs.createColorQuad(0,0,0))
        gpuRedRectangle = es.toGPUShape(bs.createColorQuad(1,0,0))
        gpuGrayCircle = es.toGPUShape(bs.createColorCircle(40,1,1,1))
        
        # Creating the main circle
        circle = sg.SceneGraphNode("circle")
        circle.childs += [gpuGrayCircle]
        
        indices =[]
        # Creating the indices
        for i in range(18):
            indice = sg.SceneGraphNode("indice"+str(i))
            indice.transform = tr.translate(0,0,0.1)
            indices.append(indice)
            #indices[i].transform = tr.scale(2,0.2,1)
            #indices[i].transform = tr.translate2(indices[i].transform,0,0.3,0)
            if i in limits:
                indices[i].childs += [gpuRedRectangle]
            else:
                indices[i].childs += [gpuBlackRectangle]
            
        # Creating the needle
        needle = Needle()
        needle.model.transform = tr.translate2(needle.model.transform,0,0.25,0.1)
        
        
        # Assembling the circle instrument
        circleInstrument = sg.SceneGraphNode("circleInstrument")
        circleInstrument.transform = tr.translate2(circle.transform,x/0.3,y/0.3,0)
        circleInstrument.childs += [circle]       
        for i in range(18):
            circleInstrument.childs += [indices[i]]
        circleInstrument.childs += [needle.model]
        
        # Rotating the indices
        for i in range(18):
            node = sg.findNode(circleInstrument,"indice"+str(i))
            node.transform = tr.rotationZ2(node.transform,-i*np.pi/9)
        
        # Scaling instrument
        scaledInstrument = sg.SceneGraphNode(name)
        scaledInstrument.transform = tr.matmul([tr.uniformScale(0.3),tr.translate(0,0,0.01)])
        scaledInstrument.childs += [circleInstrument]
        
        
    
        self.model = scaledInstrument
        self.angle = 0
        self.on = True
                
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

        
    def updateVelocity(self, velocity):
        if self.on:
            node = sg.findNode(self.model,"needle")
            self.angle = -velocity*np.pi/(180)
            node.transform = tr.rotationZ4(node.transform,self.angle,0.2,0.1,0.5)
        
    def updateHeight(self,height):
        if self.on:
            node = sg.findNode(self.model, "needle")
            angle = self.heightAngle(height)
            node.transform = tr.rotationZ4(node.transform,-angle,0.2,0.1,0.5)
        
   
    def heightAngle(self,height):
        m = (2*np.pi)/1.33
        return m*(height+0.43)
    
    def getAngle(self):
        return self.angle
    
class Needle:
    def __init__(self):
        gpuRedTriangle = es.toGPUShape(bs.createColorTriangle(1,0,0))
        
        needle = sg.SceneGraphNode("needle")
        needle.transform = tr.scale(0.1,0.5,1)
        needle.childs += [gpuRedTriangle]
        self.model = needle
    
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

        
class RectangularInstrument:
    def __init__(self,x,y,sx,sy,name,limits =[]):
        gpuGrayRectangle = es.toGPUShape(bs.createColorQuad(0.9,0.9,0.9))
        gpuBlackRectangle = es.toGPUShape(bs.createColorQuad(0,0,0))
        gpuRedRectangle = es.toGPUShape(bs.createColorQuad(1,0,0))
        
        
        #Creating a border
        rightBorder = sg.SceneGraphNode("rightBorder")
        rightBorder.transform = tr.scale(0.01,1,1)
        rightBorder.transform = tr.translate2(rightBorder.transform,0.55,0,0)
        rightBorder.childs += [gpuBlackRectangle]
        
        leftBorder = sg.SceneGraphNode("leftBorder")
        leftBorder.transform = tr.scale(0.01,1,1)
        leftBorder.transform = tr.translate2(leftBorder.transform,-0.55,0,0)
        leftBorder.childs += [gpuBlackRectangle]
        
        upBorder = sg.SceneGraphNode("upBorder")
        upBorder.transform = tr.scale(1.1,0.01,1)
        upBorder.transform = tr.translate2(upBorder.transform,0,0.505,0)
        upBorder.childs += [gpuBlackRectangle]
        
        downBorder = sg.SceneGraphNode("downBorder")
        downBorder.transform = tr.scale(1.1,0.01,1)
        downBorder.transform = tr.translate2(downBorder.transform,0,-0.505,0)
        downBorder.childs += [gpuBlackRectangle]
        
        indices = []
        for i in range(6):
            indice = sg.SceneGraphNode("indice"+str(i))
            indice.transform = tr.matmul([tr.scale(0.8,0.03,1),tr.translate(0,0,0.11)])
            if i in limits:
                indice.childs += [gpuRedRectangle]
            else:
                indice.childs += [gpuBlackRectangle]
            indices += [indice]
            
        needle = sg.SceneGraphNode("needle")
        needle.childs += [gpuRedRectangle]
           
        
        scaledRectangle = sg.SceneGraphNode("scaledRectangle")
        scaledRectangle.transform = tr.translate(0,0,-0.01)
        scaledRectangle.childs += [gpuGrayRectangle]
        
        base = sg.SceneGraphNode(name)
        base.transform = tr.scale(sx,sy,1)
        base.transform = tr.translate2(base.transform,x,y,0.1)
        
        base.childs += [rightBorder]
        base.childs += [leftBorder]
        base.childs += [upBorder]
        base.childs += [downBorder]
        base.childs += [scaledRectangle]
        for i in range(6):
            indices[i].transform = tr.translate2(indices[i].transform,0,0.4-0.16*i,0)
            base.childs += [indices[i]]
        base.childs += [needle]        

        
        self.model = base
        self.on = True
        
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

        
    
    def updateHeight(self,height):
        if self.on:
            if height >=0.9:
                Height = 0.43
            elif height <= 0:
                Height = -0.43
            else:
                Height = self.functionHeight(height)
            node = sg.findNode(self.model,"needle")
            node.transform = tr.translate3(0.8,0.05,1,0, Height,0)
        
    def updatePitching(self,angle):
        if self.on:
            (x,y) = self.functionAngle(angle)
            node = sg.findNode(self.model, "needle")
            node.transform = tr.translate3(0.1,0.1,1,x,y,0)
        

        
    def functionHeight(self,height):
        m = 2*0.43/0.9
        n = -0.43
        return m*height + n
    
    def functionAngle(self, angle):
        y = 0.43*np.sin(angle)
        x = 0.35*np.cos(angle)
        return (x,y)
    
    
class Button:
    
    def __init__(self,x,y,name):
        
        gpuRedQuad = es.toGPUShape(bs.createColorQuad(1,0,0))
        gpuGreenQuad = es.toGPUShape(bs.createColorQuad(0,1,0))
        
        button = sg.SceneGraphNode(name)
        button.transform = tr.translate3(0.3,0.3,1,x,y,0.1)
        button.childs += [gpuGreenQuad]
        self.model = button
        self.gpuRedQuad = gpuRedQuad
        self.gpuGreenQuad = gpuGreenQuad
        
    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

        
    def on(self):
        node = sg.findNode(self.model,"button")
        node.childs = [self.gpuGreenQuad]
        
    def off(self):
        node = sg.findNode(self.model,"button")
        node.childs = [self.gpuRedQuad]
        

class PanelButton:
    
    def __init__(self,x,y):
        
        gpuGrayQuad = es.toGPUShape(bs.createColorQuad(0.5,0.5,0.5))
        
        grayPanel = sg.SceneGraphNode("grayPanel")
        grayPanel.transform = tr.matmul([tr.scale(0.55,1.3,1),tr.translate(0,0,0.05)])
        grayPanel.childs += [gpuGrayQuad]
        
        motor = Button(0,0.4,"motor")
        gassoline = Button(0,0,"gassoline")
        controlButton = Button(0,-0.4,"panelButton")
        
        panel = sg.SceneGraphNode("panel")
        panel.transform = tr.translate3(0.3,0.25,1,x,y,0.001)
        panel.childs += [grayPanel]
        panel.childs += [motor.model, gassoline.model, controlButton.model]
        
        self.model = panel
        self.gpuRedQuad = es.toGPUShape(bs.createColorQuad(1,0,0))
        self.gpuGreenQuad = es.toGPUShape(bs.createColorQuad(0,1,0))
        self.stateMotor = True
        self.stateGassoline = True
        self.statePanelButton = True
    
    def draw(self, pipeline_color, projection, view):
        """
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        """
        sg.drawSceneGraphNode(self.model, pipeline_color)

        
    def on(self,button, plane, instruments):
        node = sg.findNode(self.model,button)
        node.childs = [self.gpuGreenQuad]
        
        if button == "motor" or button == "gassoline":
            plane.on = True
            
        elif button == "panelButton":
            plane.RPM = 0
            for i in range(len(instruments)):
                instruments[i].on = True
        
    def off(self, button, plane, instruments):
        node = sg.findNode(self.model, button)
        node.childs = [self.gpuRedQuad]
        
        if button == "motor" or button == "gassoline":
            plane.on = False
        
        elif button == "panelButton":
            for i in range(len(instruments)):
                instruments[i].on = False
            
        
    def changeState(self, button, plane, instruments):
        if self.state(button):
            self.off(button, plane, instruments)
        else:
            self.on(button, plane, instruments)
        
    
    def state(self, button):
        if button == "motor":
            state = self.stateMotor
            self.stateMotor = not self.stateMotor

        elif button == "gassoline":
            state = self.stateGassoline
            self.stateGassoline = not self.stateGassoline

        elif button == "panelButton":
            state = self.statePanelButton
            self.statePanelButton = not self.statePanelButton
        
        return state

class Axis(object):

    def __init__(self):
        self.model = es.toGPUShape(bs.createAxis(1))
        self.show = True

    def toggle(self):
        self.show = not self.show

    def draw(self, pipeline, projection, view):
        if not self.show:
            return
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'model'), 1, GL_TRUE, tr.identity())
        pipeline.drawShape(self.model, GL_LINES)

class Controls:
    def __init__(self):
        board = Board()
        velocimeter = CircleInstrument(-0.7,-0.75,'velocimeter',[0,1,2,3,15,16,17])
        revolutions = CircleInstrument(-0.1,-0.75,'revolutions',[15,16,17])
        height = RectangularInstrument(-0.4,-0.75,0.1,0.3,'height',[0,1])
        pitching = RectangularInstrument(0.38,-0.75,0.38,0.3,'pitching')
        panelButton = PanelButton(0.75,-0.75)

        controls = sg.SceneGraphNode("controls")
        controls.transform = tr.matmul([tr.rotationX(np.pi/2)])
        controls.childs += [board.model, velocimeter.model, revolutions.model, height.model, pitching.model, panelButton.model]

        rotatedControls = sg.SceneGraphNode("rotated")
        rotatedControls.transform = tr.matmul([tr.rotationZ(135*np.pi/180),tr.translate2(rotatedControls.transform,0,0,0)]) #-0.5,-2,-0.5
        rotatedControls.transform = tr.translate2(rotatedControls.transform, 2.2,2.2,1)  # 3.2,3.2,0
        rotatedControls.childs += [controls]

        self.model = rotatedControls
        self.x = 0
        self.y = 0
        self.z = 0

        self.velocimeter = velocimeter
        self.revolutions = revolutions
        self.height = height
        self.pitching = pitching
        self.panelButton = panelButton
        self.angle = 0 

    def draw(self, pipeline_color, projection, view):
        glUseProgram(pipeline_color.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'projection'), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_color.shaderProgram, 'view'), 1, GL_TRUE, view)
        sg.drawSceneGraphNode(self.model, pipeline_color)

    def posX(self):
        self.x += 0.05
        node = sg.findNode(self.model, "rotated")
        node.transform = tr.translate2(node.transform,0.05,0,0)

    def posY(self):
        self.y += 0.05
        node = sg.findNode(self.model, "rotated")
        node.transform = tr.translate2(node.transform,0,0.05,0)
    
    def posZ(self):
        self.z += 0.05
        node = sg.findNode(self.model, "rotated")
        node.transform = tr.translate2(node.transform,0,0,0.05)

    def update(self,velocity,RPM,height,angle):
        self.velocimeter.updateVelocity(velocity)
        self.revolutions.updateVelocity(RPM)
        self.height.updateHeight(height)
        self.pitching.updatePitching(angle)

        velocimeter = sg.findNode(self.model,"velocimeter")
        velocimeter.transform = self.velocimeter.model.transform
        revolutions = sg.findNode(self.model,"revolutions")
        revolutions.transform = self.revolutions.model.transform
        
        """
        height = sg.findNode(self.model,"height")
        height.transform = self.pitching.model.transform
        """
        """
        pitching = sg.findNode(self.model,"pitching")
        pitching.transform = self.pitching.model.transform
        """
    def rotate(self):
        self.angle += np.pi/2
        node = sg.findNode(self.model, 'controls')
        node.transform = tr.rotationX2(node.transform,self.angle)
    
    def changeState(self,button,plane,instruments):
        self.panelButton.changeState(button,plane,instruments)
        node = sg.findNode(self.model,'panel')
        #node.childs = self.panelButton

class Explosion:
    
    def __init__(self):
        
        gpuRedcube = es.toGPUShape(bs.createColorCube(1,0,0))

        prism = sg.SceneGraphNode("prism")
        prism.childs += [gpuRedcube]
        
        
        self.model = prism
        self.explosion = False
        
    def draw(self,pipeline):
        if self.explosion:
            sg.drawSceneGraphNode(self.model, pipeline)
            
    def explode(self, x, y):
        self.model.transform = tr.translate(x, y, 0)
        self.explosion = True
        
    def update(self,x,y):
        self.model.transform = tr.translate(x,0,y)
