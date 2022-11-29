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

class PlaneModel(Mesh):
    def __init__(self, nvert=40, nhoriz=40, material=Material(Ka=[0.5,0.5,0.5], Kd=[0.6,0.6,0.9], Ks=[1.,1.,0.9], Ns=15.0)):
        n = nvert*nhoriz
        vertices = np.zeros((n, 3), 'f')
        vertex_colors = np.zeros((n, 3), 'f')

        vslice = np.pi/nvert
        hslice = 2.*np.pi/nhoriz

        # texture coordinates
        textureCoords = np.zeros((n, 2), 'f')

        # start by creating vertices
        random.seed(1)
        for i in range(nvert):
            y = 1.0
            for j in range(nhoriz):
                x = random.random()
                v = i*nhoriz+j
                vertices[v, 0] = i
                
                # This ensures that the plane will be smooth
                
                z = vertices[v-1, 1] - np.sin(x)
                if (z > 0 and z <= 0.3) or z < 0 and (0 - z <= 0.3):
                    vertices[v, 1] = np.sin(x) 
                elif (z > 0):
                    vertices[v, 1] = np.sin(x)/2 + np.sin(x)  
                    
                vertices[v, 2] = j
                vertex_colors[v, 0] = float(i) / float(nvert)
                vertex_colors[v, 1] = float(j) / float(nhoriz)
                textureCoords[v, 1] = float(i) / float(nvert) *10
                textureCoords[v, 0] = float(j) / float(nhoriz) *10
     
    
        for i in range(nvert):
            for j in range(nhoriz):
                distance1 = math.sqrt((0.5*(nvert - i ))**2 + (0.5*(nhoriz - j))**2)
                distance2 = math.sqrt((0.5*(nvert/2 - i ))**2 + (0.5*(nhoriz/2 - j))**2)
                distance4 = math.sqrt((0.5*(nvert/4 - i ))**2 + (0.5*(nhoriz/4 - j))**2)
                
                # decreasing area in the middle
                if 2 > distance2:
                    v = i*nhoriz+j
                    vertices[v, 1] -= 3  
        
                # decreasing area around the edge 
                x = 1.5
                for n in range(3):
                    if  nvert/3 + n < distance4:
                        v = i*nhoriz+j
                        vertices[v, 1] -= x
                        x += 0.4

                
        # np.savetxt("./verticies.txt", vertices, "%f")
        
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
        
        self.textures.append(Texture('grass2.jpg'))