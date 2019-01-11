# -*- coding: utf-8 -*-
""" All rendering related functions and classes

"""
import os

import moderngl
from pyrr import Matrix44

from pysg.camera import Camera
from pysg.scene import Scene


class Renderer:
    def __init__(self, scene: Scene, camera: Camera):
        """Base class which takes a scene and camera and render.

        Args:
            scene (Scene): Scene which shall be rendered.
            camera (Camera): Camera which is used to view scene.

        """
        self.scene = scene
        self.camera = camera

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
        self.ctx = moderngl.create_context()

        # TODO Load also other shader
        shader_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'shader')
        vertex_shader_source = open(os.path.join(shader_path, 'simple.vert')).read()
        fragment_shader_source = open(os.path.join(shader_path, 'simple.frag')).read()
        self.prog = self.ctx.program(fragment_shader=fragment_shader_source, vertex_shader=vertex_shader_source)
        self.mvp = self.prog['Mvp']
        # TODO add light and other stuff
        # self.light = self.prog['Light']

    def render(self) -> None:
        self.ctx.viewport = self.viewport
        self.ctx.clear(*self.scene.background_color)

        # Update projection matrices
        if self.scene.auto_update:
            self.scene.update_world_matrix()

        if self.camera.parent is None:
            self.camera.update_world_matrix()

        # Render all objects
        for model_3d in self.scene.render_list:
            vert_pos = model_3d.geometry.vertex_position
            vert_idx = model_3d.geometry.vertex_indices
            vbo = self.ctx.buffer(vert_pos.astype('f4').tobytes())
            ibo = self.ctx.buffer(vert_idx.astype('i4').tobytes())
            vao_content = [
                (vbo, '3f', 'in_vert')
            ]
            vao = self.ctx.vertex_array(self.prog, vao_content, index_buffer=ibo)

            # TODO Use camera transformation matrix
            lookat = Matrix44.look_at(
                eye=(5, 3, 4),
                target=(0.0, 0.0, 0.0),
                up=(0.0, 0.0, 1.0),
            )
            self.mvp.write((self.camera.projection_matrix * lookat).astype('f4').tobytes())
            vao.render(moderngl.TRIANGLE_STRIP)


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
