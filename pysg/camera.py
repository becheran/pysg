# -*- coding: utf-8 -*-
"""Camera is needed to render a scene
"""
import math
import numpy as np

from pysg.node_3d import Node3D


class Camera(Node3D):
    """Camera in scene"""

    def __init__(self):
        """
        Args:
            TODO:
        """
        super().__init__()
        self.projection_matrix = np.zeros([3, 4], float)


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
        self._fov = fov
        self._aspect = aspect
        self._near = near
        self._far = far
        self.projection_matrix = self.compute_projection_matrix()

    def compute_projection_matrix(self):
        z = (-2.0 * self._near * self._far) / (self._far - self._near)
        y = 1.0 / math.tan(self._fov * math.pi / 360)
        x = y / self._aspect

        return np.array([
            x, 0.0, 0.0, 0.0,
            0.0, y, 0.0, 0.0,
            0.0, 0.0, -1.0, -1.0,
            0.0, 0.0, z, 0.0])


class OrthographicCamera(Camera):
    """Uses square as projection matrix"""

    def __init__(self, *, left, right, top, bottom, near, far):
        """
        Args:
            left (float):  Camera volume left (usually -screen_width/2).
            right (float):  Camera volume right (usually screen_width/2).
            top (float):  Camera volume top (usually screen_height/2).
            bottom (float):  Camera volume bottom (usually -screen_height/2)..
            near (float): Camera frustum near plane. Everything closer will be culled.
            far (float): Camera frustum far plane. Everything farther away will be culled.

        """
        super().__init__()
        self.bottom = bottom
        self.top = top
        self.right = right
        self.left = left
        self._near = near
        self._far = far
        self.projection_matrix = self.compute_projection_matrix()

    def compute_projection_matrix(self):
        z = (-2.0 * self._near * self._far) / (self._far - self._near)
        y = 1.0 / math.tan(self._fov * math.pi / 360)
        x = y / self._aspect

        return np.array([
            x, 0.0, 0.0, 0.0,
            0.0, y, 0.0, 0.0,
            0.0, 0.0, -1.0, -1.0,
            0.0, 0.0, z, 0.0])
