# -*- coding: utf-8 -*-
"""Camera is needed to render a scene
"""
from pysg.node_3d import Node3D


class Camera(Node3D):
    """Camera in scene"""

    def __init__(self):
        """
        Args:
            TODO:
        """
        pass


class PerspectiveCamera(Camera):
    """Uses frustum as projection matrix"""

    def __init__(self, *, fov, aspect, near, far):
        """
        Args:
            fov (float): Vertical field of view for the perspective camera in degrees.
            aspect (float): Aspect ratio of camera sensor. With/Height.
            near (float): Camera frustum near plane. Everything closer will be culled.
            far (float): Camera frustum far plane. Everything farther away will be culled.

        """
        super().__init__()
