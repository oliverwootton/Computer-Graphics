from BaseModel import BaseModel
from matutils import poseMatrix
# imports all openGL functions
from OpenGL.GL import *
import numpy as np
from mesh import Mesh
from material import Material
from texture import Texture
import random
import math

class SceneFrame(Mesh):
    def __init__(self, nvert=8, nhoriz=40, material=Material(Ka=[0.5,0.5,0.5], Kd=[0.6,0.6,0.9], Ks=[1.,1.,0.9], Ns=15.0)):
        n = nvert*nhoriz
        vertices = np.zeros((n, 3), 'f')
        vertex_colors = np.zeros((n, 3), 'f')

        # texture coordinates
        textureCoords = np.zeros((n, 2), 'f')

        # start by creating vertices
        random.seed(1)
        for i in range(nvert):
            y = 1.0
            for j in range(nhoriz):
                x = random.random()
                v = i*nhoriz+j
                vertices[v, 0] = 0

                # Makes a flat plane
                vertices[v, 1] = i 
                    
                vertices[v, 2] = j
                vertex_colors[v, 0] = float(i) / float(nvert)
                vertex_colors[v, 1] = float(j) / float(nhoriz)
                # Multiplier makes the texture wrap increase
                textureCoords[v, 1] = float(i) / float(nvert) *3
                textureCoords[v, 0] = float(j) / float(nhoriz) *3

        
        nfaces = 2 * (nvert-1)*(nhoriz-1)
        indices = np.zeros((nfaces, 3), dtype=np.uint32)
        k = 0

        for j in range(nvert-1):
            n = nhoriz-1
            for i in range(nhoriz-1):
                lastrow = nhoriz*(j+1)
                row = nhoriz*j
                if j%2 == 0:
                    indices[k, 2] = row + i
                    indices[k, 1] = lastrow + i
                    indices[k, 0] = row + i + 1
                    k += 1

                    indices[k, 0] = row + i + 1
                    indices[k, 1] = lastrow + i + 1
                    indices[k, 2] = lastrow + i
                    k += 1  
                else:
                    indices[k, 0] = row + n
                    indices[k, 1] = lastrow + n 
                    indices[k, 2] = row+ n - 1
                    k += 1

                    indices[k, 2] = row + n - 1
                    indices[k, 1] = lastrow + n - 1
                    indices[k, 0] = lastrow + n
                    k += 1
                    n -= 1
        
        # np.savetxt("./indices.txt", indices, "%f")
        
        Mesh.__init__(self,
                      vertices=vertices,
                      faces=indices,
                      textureCoords=textureCoords,
                      material=material
                      )
        
        # Applies the texture to the model
        self.textures.append(Texture('floor_texture.jpg'))
       