# -*- coding: utf-8 -*-
"""The root of the scene graph

All children added to this node can be rendered via a renderer.

"""
from pysg.error import ParameterError
from pysg.scene import Scene


class Renderer:
    def __init__(self, scene, camera):
        """Base class which takes a scene and camera and render.

        Args:
            scene (Scene): Scene which shall be rendered.
            camera (Camera): Camera which is used to view scene.

        """
        if type(scene) is not Scene:
            raise ParameterError(scene, "Given Scene object is not from type Scene.")

        self.scene = scene
        self.camera = camera

    def render(self):
        raise NotImplementedError()

class GLRenderer(Renderer):
    """Render the scene and the camera to a OpenGL window."""

    def __init__(self, scene, camera):
        """

        Args:
            scene:
            camera:
        """
        super().__init__(scene, camera)

    def render(self):
        pass


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

