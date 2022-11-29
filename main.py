import pygame

# import the scene class
from cubeMap import FlattenCubeMap
from scene import Scene

from lightSource import LightSource

from blender import load_obj_file

from BaseModel import DrawModelFromMesh

from shaders import *

from ShadowMapping import *

from sphereModel import Sphere

from skyBox import *

from environmentMapping import *

from planeModel import PlaneModel
from sandModel import SandModel
from waterModel import WaterModel
from sceneFrame import SceneFrame
from bottomFrame import BottomFrame

class JungleScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        # Light source position
        self.light = LightSource(self, position=[10, 10, -5])

        self.shaders='phong'

        # For shadow map rendering (creates a texture to apply to the terrain surface)
        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)

        # Variable ensures all the 
        terrain = [-5, -1, -5]
        # Creates the terrain model with shadows mapped on top
        self.terrain = DrawModelFromMesh(scene=self, M=poseMatrix(position=terrain, scale=0.25), mesh=PlaneModel(), shader=ShadowMappingShader(shadow_map=self.shadows), name='plane')
        self.sand = DrawModelFromMesh(scene=self, M=poseMatrix(position=terrain, scale=0.25), mesh=SandModel(), shader=ShadowMappingShader(shadow_map=self.shadows), name='plane')
        self.sea = DrawModelFromMesh(scene=self, M=poseMatrix(position=terrain, scale=0.25), mesh=WaterModel(), shader=PhongShader(), name='plane') 
        
        scaleFactor = 0.2507
        self.frameBottom = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-5, -2.5, -5], scale=0.25), mesh=BottomFrame(), shader=PhongShader(), name='plane') 
        self.frame = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-5, -2.5, -5.01], scale=scaleFactor), mesh=SceneFrame(), shader=PhongShader(), name='plane')
        self.frame3 = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-5, -2.5, -5], scale=scaleFactor, orientation=1.571), mesh=SceneFrame(), shader=PhongShader(), name='plane')
        self.frame2 = DrawModelFromMesh(scene=self, M=poseMatrix(position=[4.75, -2.5, 4.75], scale=scaleFactor, orientation=3.14), mesh=SceneFrame(), shader=PhongShader(), name='plane')
        self.frame4 = DrawModelFromMesh(scene=self, M=poseMatrix(position=[4.75, -2.5, 4.76], scale=scaleFactor, orientation=-1.571), mesh=SceneFrame(), shader=PhongShader(), name='plane')             
        
        # Uncomment below to show the position of the light source
        # self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=0.2), mesh=Sphere(material=Material(Ka=[10,10,10])), shader=FlatShader())
   
        # Creates the models for groups of trees and ferns
        groupOfTrees1 = load_obj_file('models/Group-of-Trees.obj')
        self.add_models_list ([DrawModelFromMesh(scene=self, M=poseMatrix(position=[-2.5, -1, -2.5], scale=0.25,), mesh=mesh, shader=PhongShader(), name='box') for mesh in groupOfTrees1])
        groupOfTrees2 = load_obj_file('models/Group-of-Trees.obj')
        self.add_models_list ([DrawModelFromMesh(scene=self, M=poseMatrix(position=[-1.5, -1, 2.25], scale=0.2,), mesh=mesh, shader=PhongShader(), name='box') for mesh in groupOfTrees2])
        groupOfTrees3 = load_obj_file('models/Group-of-Trees.obj')
        self.add_models_list ([DrawModelFromMesh(scene=self, M=poseMatrix(position=[2, -1, -2.25], scale=0.2,), mesh=mesh, shader=PhongShader(), name='box') for mesh in groupOfTrees3])
        
        # Creates the models for a line of trees on the edge of the plane
        tree1 = load_obj_file('models/line-of-trees.obj')
        self.add_models_list ([DrawModelFromMesh(scene=self, M=poseMatrix(position=[-4.5, -1, 0], scale=0.2,), mesh=mesh, shader=PhongShader(), name='box') for mesh in tree1])
        tree2 = load_obj_file('models/line-of-trees2.obj')
        self.add_models_list ([DrawModelFromMesh(scene=self, M=poseMatrix(position=[0, -1, -4.5], scale=0.2,), mesh=mesh, shader=PhongShader(), name='box') for mesh in tree2])
        
        # Creates the models for individual fern models 
        fern1 = load_obj_file('models/fern2.obj')
        self.add_models_list ([DrawModelFromMesh(scene=self, M=poseMatrix(position=[1.25, -1, 0.5], scale=0.1,), mesh=mesh, shader=PhongShader(), name='box') for mesh in fern1])
        fern2 = load_obj_file('models/fern3.obj')
        self.add_models_list ([DrawModelFromMesh(scene=self, M=poseMatrix(position=[1.3, -1, 0], scale=0.1,), mesh=mesh, shader=PhongShader(), name='box') for mesh in fern2])
        fern3 = load_obj_file('models/fern1.obj')
        self.add_models_list ([DrawModelFromMesh(scene=self, M=poseMatrix(position=[-1.2, -1, 0.5], scale=0.1,), mesh=mesh, shader=PhongShader(), name='box') for mesh in fern3])
        fern4 = load_obj_file('models/fern4.obj')
        self.add_models_list ([DrawModelFromMesh(scene=self, M=poseMatrix(position=[-1.4, -1, -1], scale=0.1,), mesh=mesh, shader=PhongShader(), name='box') for mesh in fern4])


        self.skybox = SkyBox(scene=self)
        
        self.environment = EnvironmentMappingTexture(width=400, height=400)
        self.sphere = DrawModelFromMesh(scene=self, M=poseMatrix(position=[0, 1, 0], scale=0.5), mesh=Sphere(), shader=EnvironmentShader(map=self.environment))
        
        # environment box for reflectionsenvbox
        #self.envbox = EnvironmentBox(scene=self)
        
        self.flattened_cube = FlattenCubeMap(scene=self, cube=self.environment)


    def draw_shadow_map(self):
        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # also all models from the table
        for model in self.models:
            model.draw()
            
        # # and for the box
        # for model in self.terrain:
        #     model.draw()

    def draw_reflections(self):
        
        self.skybox.draw()
        self.sea.draw()
        self.sand.draw()
        self.terrain.draw()

        for model in self.models:
            model.draw()


    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # when using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        # first, we draw the skybox
        self.skybox.draw()

        # render the shadows
        self.shadows.render(self, target=[-5, -1, 0])

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:
            # glEnable(GL_BLEND)
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            # self.envbox.draw()
            
            self.environment.update(self)
            
            # self.sphere.draw()
            
            # self.show_texture.draw()
            
            # self.show_shadow_map.draw()
        
        self.terrain.draw()
        self.sand.draw()
        self.sea.draw()
        
        self.frame.draw()
        self.frame2.draw()
        self.frame3.draw()
        self.frame4.draw()
        self.frameBottom.draw()
        
        
        # then we loop over all models in the list and draw them
        for model in self.models:
            model.draw()
        


        # # also all models from the table
        # for model in self.table:
        #     model.draw()

        # Uncomment to show ball of light
        # self.show_light.draw()

        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        '''
        Process additional keyboard events for this demo.
        '''
        Scene.keyboard(self, event)

        if event.key == pygame.K_c:
            if self.flattened_cube.visible:
                self.flattened_cube.visible = False
            else:
                print('--> showing cube map')
                self.flattened_cube.visible = True

        if event.key == pygame.K_t:
            if self.show_texture.visible:
                self.show_texture.visible = False
            else:
                print('--> showing texture map')
                self.show_texture.visible = True

        if event.key == pygame.K_s:
            if self.show_shadow_map.visible:
                self.show_shadow_map.visible = False
            else:
                print('--> showing shadow map')
                self.show_shadow_map.visible = True

        if event.key == pygame.K_1:
            print('--> using Flat shading')
            self.bunny.use_textures = True
            self.bunny.bind_shader('flat')

        if event.key == pygame.K_2:
            print('--> using Phong shading')
            self.bunny.use_textures = True
            self.bunny.bind_shader('phong')

        elif event.key == pygame.K_4:
            print('--> using original texture')
            self.bunny.shader.mode = 1

        elif event.key == pygame.K_6:
            self.bunny.mesh.material.alpha += 0.1
            print('--> bunny alpha={}'.format(self.bunny.mesh.material.alpha))
            if self.bunny.mesh.material.alpha > 1.0:
                self.bunny.mesh.material.alpha = 0.0

        elif event.key == pygame.K_7:
            print('--> no face culling')
            glDisable(GL_CULL_FACE)

        elif event.key == pygame.K_8:
            print('--> glCullFace(GL_FRONT)')
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)

        elif event.key == pygame.K_9:
            print('--> glCullFace(GL_BACK)')
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)

        elif event.key == pygame.K_BACKQUOTE:
            if glIsEnabled(GL_DEPTH_TEST):
                print('--> disable GL_DEPTH_TEST')
                glDisable(GL_DEPTH_TEST)
            else:
                print('--> enable GL_DEPTH_TEST')
                glEnable(GL_DEPTH_TEST)


if __name__ == '__main__':
    # initialises the scene object
    # scene = Scene(shaders='gouraud')
    scene = JungleScene()

    # starts drawing the scene
    scene.run()
