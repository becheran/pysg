# -*- coding: utf-8 -*-
"""Camera is used to render a scene to the screen
"""
import math

import pyrr
from pyrr import Matrix44

import pysg.math as pysg_math
from pysg.error import ParameterError
from pysg.node_3d import Node3D


class Camera(Node3D):
    """Camera in scene"""

    def __init__(self):
        """Base class of all camera types used in pysg."""

        super().__init__()
        self.__projection_matrix = pyrr.Matrix44()
        self._need_matrix_update = True

    @property
    def projection_matrix(self) -> Matrix44:
        if self._need_matrix_update:
            self._need_matrix_update = False
            self.__projection_matrix = self.compute_projection_matrix()
        return self.__projection_matrix

    def compute_projection_matrix(self) -> Matrix44:
        """ Projection matrix calculation based on different camera types.

        Returns:
            Matrix44: Projection matrix in OpenGL format.
            m0 m4 m8  m12
            m1 m5 m9  m13
            m2 m6 m10 m14
            m3 m7 m11 m15

        """
        raise NotImplementedError()


class PerspectiveCamera(Camera):
    """Uses frustum as projection matrix"""

    def __init__(self, *, fov: float, aspect: float, near: float, far: float):
        """
        Args:
            fov (float): Vertical field of view for the perspective camera in degrees.
            aspect (float): Aspect ratio of camera sensor. With/Height.
            near (float): Camera frustum near plane. Everything closer will be culled.
            far (float): Camera frustum far plane. Everything farther away will be culled.

        """
        super().__init__()

        # Check all parameter
        if fov <= 0 \
                or fov >= 180 \
                or not pysg_math.is_angle(fov, in_degrees=True, allow_negative=False, limit_to_circle=True):
            raise ParameterError(fov, 'Field of view with this value is not allowed!')
        if aspect <= 0:
            raise ParameterError(aspect, 'Aspect smaller or equals zero not allowed!')
        if near >= far:
            raise ParameterError((near, far), 'Near must be smaller than far!')
        if near <= 0:
            raise ParameterError(near, 'Near must be greater zero!')
        if far <= 0:
            raise ParameterError(far, 'Far must be greater zero!')

        self.__fov = fov
        self.__aspect = aspect
        self.__near = near
        self.__far = far

    def compute_projection_matrix(self) -> Matrix44:
        """ Projection matrix calculation for the perspective camera.
            Based on: https://glumpy.github.io/modern-gl.html#projection-matrix
            Only difference is that we use the horizontal FOV not vertical
        """

        near_minus_far = self.__near - self.__far
        f = 1 / math.tan(self.__fov / 2)
        aspect_reciprocal = 1 / self.__aspect

        m00 = f
        m11 = f / aspect_reciprocal
        m22 = (self.__far + self.__near) / near_minus_far
        m32 = (2 * self.__near * self.__far) / near_minus_far

        return Matrix44([
            m00, 0.0, 0.0, 0.0,
            0.0, m11, 0.0, 0.0,
            0.0, 0.0, m22, -1,
            0.0, 0.0, m32, 0.0])


class OrthographicCamera(Camera):
    """Uses square as projection matrix"""

    def __init__(self, *, left: float, right: float, top: float, bottom: float, near: float, far: float):
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

        # Check all parameter
        if left >= right:
            raise ParameterError((left, right), 'Left must be smaller than right!')
        if near >= far:
            raise ParameterError((near, far), 'Near must be smaller than far!')
        if bottom >= top:
            raise ParameterError((top, bottom), 'Bottom must be smaller than top!')
        if near <= 0:
            raise ParameterError(near, 'Near must be greater zero!')
        if far <= 0:
            raise ParameterError(far, 'Far must be greater zero!')

        self.__bottom = bottom
        self.__top = top
        self.__right = right
        self.__left = left
        self.__near = near
        self.__far = far

    def compute_projection_matrix(self) -> Matrix44:
        """ Projection matrix calculation for the orthographic camera.
                Based on: https://glumpy.github.io/modern-gl.html#projection-matrix
        """

        right_minus_left = self.__right - self.__left
        top_minus_bottom = self.__top - self.__bottom
        far_minus_near = self.__far - self.__near

        m00 = 2 / right_minus_left
        m11 = 2 / top_minus_bottom
        m22 = -2 / far_minus_near

        m30 = -(self.__right + self.__left) / right_minus_left
        m31 = -(self.__top + self.__bottom) / top_minus_bottom
        m32 = -(self.__far + self.__near) / far_minus_near

        return Matrix44([
            m00, 0.0, 0.0, 0.0,
            0.0, m11, 0.0, 0.0,
            0.0, 0.0, m22, 0.0,
            m30, m31, m32, 1.0])
