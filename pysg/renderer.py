# -*- coding: utf-8 -*-
"""The root of the scene graph

All children added to this node can be rendered via a renderer.

"""
import moderngl

from pysg.camera import Camera
from pysg.error import ParameterError
from pysg.scene import Scene


class Renderer:
    def __init__(self, scene, camera):
        """Base class which takes a scene and camera and render.

        Args:
            scene (Scene): Scene which shall be rendered.
            camera (Camera): Camera which is used to view scene.

        """

        if not issubclass(type(scene), Scene):
            raise ParameterError(scene, "Given scene object is not from type Scene.")
        if not issubclass(type(camera), Camera):
            raise ParameterError(camera, "Given camera object is not from type Camera.")

        self.scene = scene
        self.camera = camera

    def render(self):
        raise NotImplementedError()


class GLRenderer(Renderer):

    def __init__(self, scene, camera):
        """Render the scene to a given viewport."""
        super().__init__(scene, camera)
        # Viewport is a tuple of size four (x, y, width, height).
        self.viewport = None
        self.ctx = moderngl.create_context()

        # TODO Load also other shader
        vertex_shader_source = open('shader/simple.vert').read()
        fragment_shader_source = open('shader/simple.frag').read()
        self.prog = self.ctx.program(fragment_shader=fragment_shader_source, vertex_shader=vertex_shader_source)
        self.mvp = self.prog['Mvp']
        self.light = self.prog['Light']

    def render(self):
        self.ctx.viewport = self.viewport
        self.ctx.clear(*self.scene.background_color)

        if self.scene.auto_update:
            self.scene.update_world_matrix()

        if self.camera.parent is None:

        #TODO self.mvp.write((self.camera.projection_matrix() * self.camera.).astype('f4').tobytes())
        #TODO self.vao.render(moderngl.LINES, 65 * 4)


class HeadlessGLRenderer(Renderer):
    """Render the scene to a framebuffer which can be read to CPU RAM to be used as an image."""

    def __init__(self, scene, camera, *, width, height):
        """

        Args:
            scene:
            camera:
        """

        super().__init__(scene, camera)
        self.width = width
        self.height = height

    def render(self):
        # TODO
        pass
