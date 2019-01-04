# -*- coding: utf-8 -*-
"""The root of the scene graph

All children added to this node can be rendered via a renderer.

"""

import moderngl


class GLRenderer:
    """Render the scene and the camera to a OpenGL window."""

    def __init__(self, scene, camera):
        """

        Args:
            scene:
            camera:
        """
        self.scene = scene
        self.camera = camera


class HeadlessGLRenderer:
    """Render the scene to a framebuffer which can be read to CPU RAM to be used as an image."""

    def __init__(self, scene, camera, *, width, height):
        """

        Args:
            scene:
            camera:
        """
        self.scene = scene
        self.camera = camera
        self.width = width
        self.height = height
