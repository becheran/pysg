""" Contains some math functions."""
import math
from typing import List

import numpy as np
import pyrr
from pyrr import Matrix44, Quaternion, Vector3


def is_angle(angle, *, in_degrees, allow_negative, limit_to_circle):
    """ Check whether the given number is a valid angle rotation

    Args:
        angle (float): Number that needs to be evaluated.
        in_degrees (bool): If True expect number in degrees. Otherwise expect radians.
        allow_negative (bool): If False, no negative angles are allowed.
        limit_to_circle (bool): Determine whether the angle should be within a full circle.

    Returns:
        bool: True for valid angle, False otherwise.

    """
    if limit_to_circle:
        upper_limit = 360.0 if in_degrees else 2 * math.pi
        lower_limit = -360.0 if allow_negative else 0.0
    else:
        upper_limit = math.inf
        lower_limit = -math.inf if allow_negative else 0.0
    return lower_limit <= angle <= upper_limit


def ray_intersect_sphere(ray: np.array, sphere: np.array) -> list:
    """ Returns the intersection points of a ray and a sphere.
    See: https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection
    The ray is defined via the following equation O+tD. Where O is the origin point and D is a direction vector.
    A sphere is defined as |P−C|^2=R2 where P is the origin and C is the center of the sphere.
    R is the radius of the sphere.

    Args:
        ray: Ray geometry
        sphere: Sphere geometry

    Returns:
        list: Intersection points as 3D vector list

    """
    sphere_center = pyrr.sphere.position(sphere)
    sphere_radius = pyrr.sphere.radius(sphere)
    ray_origin = pyrr.ray.position(ray)
    ray_direction = pyrr.ray.direction(ray)

    a = 1
    b = 2 * np.dot(ray_direction, (ray_origin - sphere_center))
    c = np.dot(ray_origin - sphere_center, ray_origin - sphere_center) - sphere_radius * sphere_radius

    t_list = solve_quadratic_equation(a, b, c)

    ret = list()
    for t in t_list:
        # We are calculating intersection for ray not line! Use only positive t for ray.
        if t >= 0:
            ret.append(ray_origin + ray_direction * t)
    return ret


def solve_quadratic_equation(a: float, b: float, c: float) -> List[float]:
    """ Simple quadratic equation solver.
    Solve function of form f(x) = ax^2 + bx + c

    Args:
        a: Quadratic part of equation
        b: Linear part of equation
        c: Static part of equation
    Returns:
        List[float]: List contains either two elements for two solutions, one element for one solution, or is empty if
        no solution for the quadratic equation exists.
    """
    delta = b * b - 4 * a * c
    if delta > 0:
        # Two solutions
        # See https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection
        # Why not use simple form:
        # s1 = (-b + math.sqrt(delta)) / (2 * a)
        # s2 = (-b - math.sqrt(delta)) / (2 * a)
        q = -0.5 * (b + math.sqrt(delta)) if b > 0 else -0.5 * (b - math.sqrt(delta))
        s1 = q / a
        s2 = c / q
        return [s1, s2]
    elif delta == 0:
        # One solution
        return [-b / (2 * a)]
    else:
        # No solution exists
        return list()


# TODO Fork request to Pyrr
def compose_matrix(position: Vector3, quaternion: Quaternion, scale: Vector3) -> Matrix44:
    """ Reconstruct a 4x4 matrix from rotation, position and scale.

    Note that all matrices are in the OpenGL column first layout.

    Args:
        quaternion: Input rotation in Quaternion representation.
        position: Position in 3D space as Vector3.
        scale: Scale of object (x, y, and z) as Vector3.
    """

    translation_matrix = Matrix44([[1., 0., 0., 0.],
                                   [0., 1., 0., 0.],
                                   [0., 0., 1., 0.],
                                   [position[0], position[1], position[2], 1.]])
    rotation_matrix = quaternion.matrix44
    scale_matrix = Matrix44([[scale[0], 0., 0., 0.0],
                             [0., scale[1], 0., 0.0],
                             [0., 0., scale[2], 0.0],
                             [0., 0., 0., 1.]])
    return translation_matrix * rotation_matrix * scale_matrix


# TODO move to pyrr
def quaternion_are_equal(q1: Quaternion, q2: Quaternion, epsilon: float = 1e-12) -> bool:
    """ Check whether two quaternions represent the same rotation.

    Note that q = -q

    Args:
        epsilon (float): Wiggle factor for rounding inaccuracy.
        q1: First quaternion.
        q2: Second quaternion.
    Returns:
        bool: True if both are equal. False if not.
    """

    return math.fabs(q1.dot(q2)) > 1 - epsilon
