# -*- coding: utf-8 -*-
""" All rendering related functions and classes

"""
import os

import moderngl

from pysg.camera import Camera
from pysg.scene import Scene
import numpy as np


class Renderer:
    def __init__(self, scene: Scene, camera: Camera):
        """Base class which takes a scene and camera and render.

        Args:
            scene (Scene): Scene which shall be rendered.
            camera (Camera): Camera which is used to view scene.

        """
        self.scene = scene
        self.camera = camera
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.CULL_FACE)
        self.ctx.front_face = 'ccw'
        self.ctx.enable(moderngl.DEPTH_TEST)

    def render(self):
        raise NotImplementedError()


class GLRenderer(Renderer):

    def __init__(self, scene: Scene, camera: Camera):
        """Render the scene to a given viewport.

        Args:
            scene (Scene): Scene which shall be rendered.
            camera (Camera): Camera which is used to view scene.
        """
        super().__init__(scene, camera)
        # Viewport is a tuple of size four (x, y, width, height).
        self.viewport = None

        # TODO Load also other shader
        shader_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'shader')
        vertex_shader_source = open(os.path.join(shader_path, 'simple.vert')).read()
        fragment_shader_source = open(os.path.join(shader_path, 'simple.frag')).read()
        self.prog = self.ctx.program(fragment_shader=fragment_shader_source, vertex_shader=vertex_shader_source)
        print(self.prog.geometry_input)

        self.mvp = self.prog['Mvp']
        self.color = self.prog['Color']
        # TODO add light and other stuff
        # self.light = self.prog['Light']

    def render(self) -> None:
        self.ctx.viewport = self.viewport
        self.ctx.clear(*self.scene.background_color)

        # Update projection matrices
        if self.scene.auto_update:
            self.scene.update_world_matrix()

        if self.camera._parent is None:
            self.camera.update_world_matrix()

        view_projection_matrix = self.camera.projection_matrix * self.camera.world_matrix.inverse

        # Render all objects
        for model_3d in self.scene.render_list:
            self.color.value = model_3d.material.color
            # TODO create buffers in geometry
            vbo = self.ctx.buffer(model_3d.geometry.vertices_position.astype('f4').tobytes())
            ibo = self.ctx.buffer(model_3d.geometry.vertex_indices.astype('i4').tobytes())
            vao_content = [
                (vbo, '3f', 'in_vert')
            ]
            vao = self.ctx.vertex_array(self.prog, vao_content, index_buffer=ibo)
            mvp = view_projection_matrix * model_3d.world_matrix
            self.mvp.write(mvp.astype('f4').tobytes())
            vao.render(moderngl.TRIANGLES)


class HeadlessGLRenderer(Renderer):

    def __init__(self, scene: Scene, camera: Camera, *, width: int, height: int):
        """Render the scene to a framebuffer which can be read to CPU RAM to be used as an image.

        Args:
            scene (Scene): Scene which shall be rendered.
            camera (Camera): Camera which is used to view scene.
            width (float): Width of output image in pixel
            height (float): Height of output image in pixel
        """

        super().__init__(scene, camera)
        self.width = width
        self.height = height

    def render(self) -> None:
        # TODO
        pass
