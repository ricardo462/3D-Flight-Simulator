"""
Daniel Calderon, CC3501, 2019-1
vertices and indices for simple shapes
"""
import numpy as np

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, textureFileName=None):
        self.vertices = vertices
        self.indices = indices
        self.textureFileName = textureFileName


def createAxis(length=1.0):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -length, 0.0, 0.0, 0.0, 0.0, 0.0,
        length, 0.0, 0.0, 1.0, 0.0, 0.0,

        0.0, -length, 0.0, 0.0, 0.0, 0.0,
        0.0, length, 0.0, 0.0, 1.0, 0.0,

        0.0, 0.0, -length, 0.0, 0.0, 0.0,
        0.0, 0.0, length, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1,
        2, 3,
        4, 5]

    return Shape(vertices, indices)

def createColorTriangle(r,g,b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -0.5, -0.5, 0.0,  r,g,b,
         0.5, -0.5, 0.0,  r,g,b,
         0.0,  0.5, 0.0,  r,g,b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return Shape(vertices, indices)


def createRainbowTriangle():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        0.0, 0.5, 0.0, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return Shape(vertices, indices)


def createRainbowQuad():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.0, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.0, 1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createColorQuad(r, g, b):
    # Defining locations and colors for each vertex of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, r, g, b,
        0.5, -0.5, 0.0, r, g, b,
        0.5, 0.5, 0.0, r, g, b,
        -0.5, 0.5, 0.0, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createTextureQuad(image_filename, nx=1, ny=1):
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions        texture
        -0.5, -0.5, 0.0, 0, 0,
        0.5, -0.5, 0.0, nx, 0,
        0.5, 0.5, 0.0, nx, ny,
        -0.5, 0.5, 0.0, 0, ny]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    textureFileName = image_filename

    return Shape(vertices, indices, textureFileName)

def createColorCircle(numVertices,r,g,b):
    vertices = [0, 0, 0.1, r, g, b]
    indices = []
    angle = 0
    dAngle = 2*(np.pi)/numVertices
    while angle <= 2*np.pi:
        vertices += [0.5*np.sin(angle), 0.5*np.cos(angle),0, r, g, b]
        angle += dAngle
    #indices += [0]
    indice = 1
    while indice < numVertices:
        indices += [0,indice,indice+1]
        indice += 1
    indices += [0,indice,1]
    return Shape(vertices,indices)


def createRainbowCube():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions         colors
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.5, 1.0, 1.0, 1.0,

        -0.5, -0.5, -0.5, 1.0, 1.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 0.0, 1.0,
        -0.5, 0.5, -0.5, 1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createColorCube(r, g, b):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -0.5, -0.5, 0.5, r, g, b,
        0.5, -0.5, 0.5, r, g, b,
        0.5, 0.5, 0.5, r, g, b,
        -0.5, 0.5, 0.5, r, g, b,

        -0.5, -0.5, -0.5, r, g, b,
        0.5, -0.5, -0.5, r, g, b,
        0.5, 0.5, -0.5, r, g, b,
        -0.5, 0.5, -0.5, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)

def createPyramid(r,g,b):
    vertices = [
        0, 0, 0, r, g,b,
        0.5, 0, 0, r, g, b,
        0.5, 0.5, 0, r, g, b,
        0, 0.5, 0, r, g, b,
        0.25, 0.25, 0.5, r, g, b
    ]

    indices = [
        0,1,4,
        1,2,4,
        2,3,4,
        3,0,4
    ]
    return Shape(vertices,indices)

def crateTriangularPrism(r,g,b):

    vertices = [
        0,0,0,r,g,b,
        0.5,0,0,r,g,b,
        0.5,0.5,0,r,g,b,
        0,0.5,0,r,g,b,
        0,0.5,0.5,r,g,b,
        0,0,0.5,r,g,b
    ]

    indices = [
        0,1,5,
        0,2,1,
        0,2,3,
        0,4,3,
        0,4,5,
        2,3,4,
        1,5,2,
        2,5,4
    ]
    return Shape(vertices,indices)
    


def createTextureCube(image_filename):
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5, 0.5, 0, 0,
        0.5, -0.5, 0.5, 1, 0,
        0.5, 0.5, 0.5, 1, 1,
        -0.5, 0.5, 0.5, 0, 1,

        # Z-
        -0.5, -0.5, -0.5, 0, 0,
        0.5, -0.5, -0.5, 1, 0,
        0.5, 0.5, -0.5, 1, 1,
        -0.5, 0.5, -0.5, 0, 1,

        # X+
        0.5, -0.5, -0.5, 0, 0,
        0.5, 0.5, -0.5, 1, 0,
        0.5, 0.5, 0.5, 1, 1,
        0.5, -0.5, 0.5, 0, 1
        ,

        # X-
        -0.5, -0.5, -0.5, 0, 0,
        -0.5, 0.5, -0.5, 1, 0,
        -0.5, 0.5, 0.5, 1, 1,
        -0.5, -0.5, 0.5, 0, 1,

        # Y+
        -0.5, 0.5, -0.5, 0, 0,
        0.5, 0.5, -0.5, 1, 0,
        0.5, 0.5, 0.5, 1, 1,
        -0.5, 0.5, 0.5, 0, 1,

        # Y-
        -0.5, -0.5, -0.5, 0, 0,
        0.5, -0.5, -0.5, 1, 0,
        0.5, -0.5, 0.5, 1, 1,
        -0.5, -0.5, 0.5, 0, 1
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices, image_filename)


def createRainbowNormalsCube():
    sq3 = 0.57735027

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0, -sq3, -sq3, sq3,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0, sq3, -sq3, sq3,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0, sq3, sq3, sq3,
        -0.5, 0.5, 0.5, 1.0, 1.0, 1.0, -sq3, sq3, sq3,

        -0.5, -0.5, -0.5, 1.0, 1.0, 0.0, -sq3, -sq3, -sq3,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0, sq3, -sq3, -sq3,
        0.5, 0.5, -0.5, 1.0, 0.0, 1.0, sq3, sq3, -sq3,
        -0.5, 0.5, -0.5, 1.0, 1.0, 1.0, -sq3, sq3, -sq3]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               4, 5, 1, 1, 0, 4,
               6, 7, 3, 3, 2, 6,
               5, 6, 2, 2, 1, 5,
               7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createColorNormalsCube(r, g, b):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions         colors   normals
        # Z+
        -0.5, -0.5, 0.5, r, g, b, 0, 0, 1,
        0.5, -0.5, 0.5, r, g, b, 0, 0, 1,
        0.5, 0.5, 0.5, r, g, b, 0, 0, 1,
        -0.5, 0.5, 0.5, r, g, b, 0, 0, 1,

        # Z-
        -0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5, 0.5, -0.5, r, g, b, 0, 0, -1,
        -0.5, 0.5, -0.5, r, g, b, 0, 0, -1,

        # X+
        0.5, -0.5, -0.5, r, g, b, 1, 0, 0,
        0.5, 0.5, -0.5, r, g, b, 1, 0, 0,
        0.5, 0.5, 0.5, r, g, b, 1, 0, 0,
        0.5, -0.5, 0.5, r, g, b, 1, 0, 0,

        # X-
        -0.5, -0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5, 0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5, 0.5, 0.5, r, g, b, -1, 0, 0,
        -0.5, -0.5, 0.5, r, g, b, -1, 0, 0,

        # Y+
        -0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5, 0.5, r, g, b, 0, 1, 0,
        -0.5, 0.5, 0.5, r, g, b, 0, 1, 0,

        # Y-
        -0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5, 0.5, r, g, b, 0, -1, 0,
        -0.5, -0.5, 0.5, r, g, b, 0, -1, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)


def createTextureNormalsCube(image_filename):
    # Defining locations,texture coordinates and normals for each vertex of the shape
    vertices = [
        #   positions            tex coords   normals
        # Z+
        -0.5, -0.5, 0.5, 0, 0, 0, 0, 1,
        0.5, -0.5, 0.5, 1, 0, 0, 0, 1,
        0.5, 0.5, 0.5, 1, 1, 0, 0, 1,
        -0.5, 0.5, 0.5, 0, 1, 0, 0, 1,
        # Z-
        -0.5, -0.5, -0.5, 0, 0, 0, 0, -1,
        0.5, -0.5, -0.5, 1, 0, 0, 0, -1,
        0.5, 0.5, -0.5, 1, 1, 0, 0, -1,
        -0.5, 0.5, -0.5, 0, 1, 0, 0, -1,

        # X+
        0.5, -0.5, -0.5, 0, 0, 1, 0, 0,
        0.5, 0.5, -0.5, 1, 0, 1, 0, 0,
        0.5, 0.5, 0.5, 1, 1, 1, 0, 0,
        0.5, -0.5, 0.5, 0, 1, 1, 0, 0,
        # X-
        -0.5, -0.5, -0.5, 0, 0, -1, 0, 0,
        -0.5, 0.5, -0.5, 1, 0, -1, 0, 0,
        -0.5, 0.5, 0.5, 1, 1, -1, 0, 0,
        -0.5, -0.5, 0.5, 0, 1, -1, 0, 0,
        # Y+
        -0.5, 0.5, -0.5, 0, 0, 0, 1, 0,
        0.5, 0.5, -0.5, 1, 0, 0, 1, 0,
        0.5, 0.5, 0.5, 1, 1, 0, 1, 0,
        -0.5, 0.5, 0.5, 0, 1, 0, 1, 0,
        # Y-
        -0.5, -0.5, -0.5, 0, 0, 0, -1, 0,
        0.5, -0.5, -0.5, 1, 0, 0, -1, 0,
        0.5, -0.5, 0.5, 1, 1, 0, -1, 0,
        -0.5, -0.5, 0.5, 0, 1, 0, -1, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices, image_filename)