# -*- coding: utf-8 -*-
""" Create basic geometries which are used to create buffered primitives in vRAM."""
import math
from typing import Tuple

import numpy as np


def create_cube(dtype='float32') -> Tuple[np.array, np.array, np.array]:
    """ Create standard cube of size one.

    Args:
        dtype: Data type of output numpy array.

    Returns:
        Tuple[np.array,np.array,np.array]: Tuple of size 3. First is np array for vertices, second for indices,
        and last for the normals.

    """
    # half dimension
    width = 0.5
    height = 0.5
    depth = 0.5

    vertices = np.array([
        # front
        # top right
        (width, height, depth),
        # top left
        (-width, height, depth),
        # bottom left
        (-width, -height, depth),
        # bottom right
        (width, -height, depth),

        # right
        # top right
        (width, height, -depth),
        # top left
        (width, height, depth),
        # bottom left
        (width, -height, depth),
        # bottom right
        (width, -height, -depth),

        # back
        # top right
        (-width, height, -depth),
        # top left
        (width, height, -depth),
        # bottom left
        (width, -height, -depth),
        # bottom right
        (-width, -height, -depth),

        # left
        # top right
        (-width, height, depth),
        # top left
        (-width, height, -depth),
        # bottom left
        (-width, -height, -depth),
        # bottom right
        (-width, -height, depth),

        # top
        # top right
        (width, height, -depth),
        # top left
        (-width, height, -depth),
        # bottom left
        (-width, height, depth),
        # bottom right
        (width, height, depth),

        # bottom
        # top right
        (width, -height, depth),
        # top left
        (-width, -height, depth),
        # bottom left
        (-width, -height, -depth),
        # bottom right
        (width, -height, -depth),
    ], dtype=dtype)

    # For triangle type counter clockwise
    # top right -> top left -> bottom left
    # top right -> bottom left -> bottom right
    indices = np.tile(np.array([0, 1, 2, 0, 2, 3], dtype='int'), (6, 1))
    for face in range(6):
        indices[face] += (face * 4)
    indices.shape = (-1,)

    normals = np.array([
        # front
        (0, 0, 1,),
        (0, 0, 1,),
        (0, 0, 1,),
        (0, 0, 1,),

        # right
        (1, 0, 0,),
        (1, 0, 0,),
        (1, 0, 0,),
        (1, 0, 0,),

        # back
        (0, 0, -1,),
        (0, 0, -1,),
        (0, 0, -1,),
        (0, 0, -1,),

        # left
        (-1, 0, 0,),
        (-1, 0, 0,),
        (-1, 0, 0,),
        (-1, 0, 0,),

        # top
        (0, 1, 0,),
        (0, 1, 0,),
        (0, 1, 0,),
        (0, 1, 0,),

        # bottom
        (0, -1, 0,),
        (0, -1, 0,),
        (0, -1, 0,),
        (0, -1, 0,),
    ], dtype=dtype)

    return vertices, indices, normals


def create_icosahedron(dtype='float32') -> Tuple[np.array, np.array, np.array]:
    """ Create icosahedron geometry with radius one.
    seealso:: http://www.songho.ca/opengl/gl_sphere.html

    Args:
        dtype: Data type of output numpy array.

    Returns:
        Tuple[np.array,np.array,np.array]: Tuple of size 3. First is np array for vertices, second for indices,
        and last for the normals.

    """
    # Fixed radius of 1
    RADIUS = 1.

    h_angle_steps = math.pi / 180 * 72  # 72 degree = 360 / 5
    v_angle_steps = math.atan(1. / 2.)  # elevation = 26.565 degree

    vertices = np.zeros((60, 3), dtype=dtype)  # array of 60 vertices (20 triangles)
    h_angle_1st_row = -math.pi / 2. - h_angle_steps / 2.  # start from -126 deg at 1st row
    h_angle_2nd_row = -math.pi / 2.  # start from -90 deg at 2nd row
    normals = np.zeros((60, 3), dtype=dtype)

    # Top vertex at(0, 0, r)
    v_top = np.array([0, 0, RADIUS])

    # 10 vertices at 1st and 2nd rows
    z = RADIUS * math.sin(v_angle_steps)  # elevation
    xy = RADIUS * math.cos(v_angle_steps)  # length on XY plane
    v_1st_row = np.zeros((5, 3))
    v_2nd_row = np.zeros((5, 3))
    for idx in range(0, 5):
        x_1 = xy * math.cos(h_angle_1st_row)
        x_2 = xy * math.cos(h_angle_2nd_row)
        y_1 = xy * math.sin(h_angle_1st_row)
        y_2 = xy * math.sin(h_angle_2nd_row)
        v_1st_row[idx] = np.array([x_1, y_1, z])
        v_2nd_row[idx] = np.array([x_2, y_2, -z])

        # next horizontal angles
        h_angle_1st_row += h_angle_steps
        h_angle_2nd_row += h_angle_steps

    # Bottom vertex at (0, 0, -r)
    v_bottom = np.array([0., 0., -RADIUS])

    # Helper function
    def set_normals(v_idx):
        v1 = vertices[v_idx] - vertices[v_idx + 1]
        v2 = vertices[v_idx] - vertices[v_idx + 2]
        normals[v_idx: v_idx + 2] = np.cross(v1, v2)

    # Set vertices and normals
    for idx in range(0, 5):
        # Top
        v_idx = idx * 3
        next_idx = (idx + 1) % 5
        vertices[v_idx] = v_top
        vertices[v_idx + 1] = v_1st_row[idx]
        vertices[v_idx + 2] = v_1st_row[next_idx]
        set_normals(v_idx)

        # First row
        v_idx = idx * 3 + (5 * 3)
        vertices[v_idx] = v_1st_row[next_idx]
        vertices[v_idx + 1] = v_1st_row[idx]
        vertices[v_idx + 2] = v_2nd_row[idx]
        set_normals(v_idx)

        # Second row
        v_idx = idx * 3 + (10 * 3)
        vertices[v_idx] = v_2nd_row[idx]
        vertices[v_idx + 1] = v_2nd_row[next_idx]
        vertices[v_idx + 2] = v_1st_row[next_idx]
        set_normals(v_idx)

        # Bottom
        v_idx = idx * 3 + (15 * 3)
        vertices[v_idx] = v_bottom
        vertices[v_idx + 1] = v_2nd_row[next_idx]
        vertices[v_idx + 2] = v_2nd_row[idx]
        set_normals(v_idx)

    indices = np.arange(0, 60, dtype='int')

    return vertices, indices, normals


def create_plane(dtype='float32') -> Tuple[np.array, np.array, np.array]:
    """ Create standard plane of size one.

    Args:
        dtype: Data type of output numpy array.

    Returns:
        Tuple[np.array,np.array,np.array]: Tuple of size 3. First is np array for vertices, second for indices,
        and last for the normals.

    """
    # half dimension
    width = 0.5
    height = 0.5

    vertices = np.array([
        # top right
        (width, 0.0, -height),
        # top left
        (-width, 0.0, -height),
        # bottom left
        (-width, 0.0, height),
        # bottom right
        (width, 0.0, height),
    ], dtype=dtype)

    # For triangle type counter clockwise
    # top right -> top left -> bottom left
    # top right -> bottom left -> bottom right
    indices = np.array([0, 1, 2, 0, 2, 3], dtype='int')

    normals = np.array([
        (0, 1, 0,),
        (0, 1, 0,),
        (0, 1, 0,),
        (0, 1, 0,)
    ], dtype=dtype)

    return vertices, indices, normals


def create_circle(dtype='float32', radius=1., fan_vertices=40) -> Tuple[np.array, np.array, np.array]:
    """ Create standard circle with radius one.

    Args:
        radius: Radius of circle.
        fan_vertices: Number of vertices used for triangle fan.
        dtype: Data type of output numpy array.

    Returns:
        Tuple[np.array,np.array,np.array]: Tuple of size 3. First is np array for vertices, second for indices,
        and last for the normals.

    """

    vertices = np.zeros((1 + fan_vertices, 3), dtype=dtype)
    vertices[0] = (0., 0., 0.)

    angle_step = (2 * math.pi) / fan_vertices
    angle = 0
    for idx in range(1, fan_vertices + 1):
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        vertices[idx] = (x, 0., y)
        angle += angle_step

    indices = np.arange(0, 1 + fan_vertices, dtype='int')[::-1]

    normals = np.array([(0, 1, 0,), ] * (fan_vertices + 1), dtype=dtype)

    return vertices, indices, normals


def create_triangle(dtype='float32') -> Tuple[np.array, np.array, np.array]:
    """ Create standard triangle with side length one.

    Args:
        dtype: Data type of output numpy array.

    Returns:
        Tuple[np.array,np.array,np.array]: Tuple of size 3. First is np array for vertices, second for indices,
        and last for the normals.

    """

    h = 0.5 * math.sqrt(3)
    inner_circle_radius = math.sqrt(3) / 6.
    vertices = np.array([
        (0, 0, h - inner_circle_radius),
        (0.5, 0, -inner_circle_radius),
        (-0.5, 0, -inner_circle_radius),
    ], dtype=dtype)

    indices = np.arange(0, 3, dtype='int')

    normals = np.array([(0, 1, 0,), ] * 3, dtype=dtype)

    return vertices, indices, normals


def create_cylinder(dtype='float32') -> Tuple[np.array, np.array, np.array]:
    """ Create standard cylinder with height two and radius one.

    Args:
        dtype: Data type of output numpy array.

    Returns:
        Tuple[np.array,np.array,np.array]: Tuple of size 3. First is np array for vertices, second for indices,
        and last for the normals.

    """

    height = 2.
    radius = 1.
    sides = 6

    # Top and bottom share one center vertices and the triangles form a fan.
    # Each sides needs two unique triangle to render correct normals
    # Vertices layout: (top (1), upper_circle (sides), middle (4*sides)  ,lower_circle (sides), bottom (1).
    vertices = np.zeros((sides * 6 + 2, 3), dtype=dtype)
    normals = np.zeros(vertices.shape, dtype=dtype)
    # Every side has 4 triangles (two for middle, one for top, and one for bottom).
    indices = np.zeros((sides * 4, 3), dtype='int')

    y = height / 2.
    vertices[0] = (0., y, 0.)
    normals[0] = (0, 1, 0)
    vertices[-1] = (0., -y, 0.)
    normals[-1] = (0, -1, 0)
    angle_step = (2 * math.pi) / sides
    angle = 0
    for idx in range(1, sides + 1):
        x = math.cos(angle) * radius
        z = math.sin(angle) * radius
        # Top circle
        vertices[idx] = (x, y, z)
        normals[idx] = (0, 1, 0)
        # Bottom circle
        vertices[idx + (sides * 5)] = (x, -y, z)
        normals[-idx - 1] = (0, -1, 0)
        angle += angle_step

    # Top indices
    indices[0:sides] = [(0, (i + 1) % sides + 1, i + 1) for i in range(sides)]
    # Bottom indices
    offset = len(vertices) - 1
    indices[-sides:] = [(offset, offset - sides + i, offset - sides + (i + 1) % sides) for i in range(sides)]

    for idx in range(0, sides):
        array_idx = sides + idx * 4 + 1
        top_left = vertices[idx + 1]
        next_idx_top = idx + 2 if idx + 1 < sides else 1
        top_right = vertices[next_idx_top]
        bottom_left = vertices[idx - sides - 1]
        next_idx_bottom = idx - sides if idx - sides <= -2 else -sides - 1
        bottom_right = vertices[next_idx_bottom]

        vertices[array_idx] = top_left
        vertices[array_idx + 1] = top_right
        vertices[array_idx + 2] = bottom_left
        vertices[array_idx + 3] = bottom_right
        v1 = top_right - top_left
        v2 = bottom_left - top_left
        normal = np.cross(v1, v2) / np.linalg.norm(np.cross(v1, v2))
        normals[array_idx: (array_idx + 4)] = normal

        indices[sides + idx] = (array_idx, array_idx + 1, array_idx + 2)
        indices[sides * 2 + idx] = (array_idx + 1, array_idx + 3, array_idx + 2)

    indices = indices.flatten()

    return vertices, indices, normals


def create_tetrahedral(dtype='float32') -> Tuple[np.array, np.array, np.array]:
    """ Create tetrahedral geometry with radius one.

    Args:
        dtype: Data type of output numpy array.

    Returns:
        Tuple[np.array,np.array,np.array]: Tuple of size 3. First is np array for vertices, second for indices,
        and last for the normals.

    """
    size = 0.5

    v1 = np.array((size, size, size))
    v2 = np.array((size, -size, -size))
    v3 = np.array((-size, size, -size))
    v4 = np.array((-size, -size, size))

    vertices = np.array([
        # 1
        v4,
        v3,
        v2,

        # 2
        v3,
        v4,
        v1,

        # 3
        v1,
        v4,
        v2,

        # 4
        v2,
        v3,
        v1,
    ], dtype=dtype)

    norm_1 = tuple(np.cross((v4 - v2), (v3 - v2)))
    norm_2 = tuple(np.cross((v3 - v1), (v4 - v1)))
    norm_3 = tuple(np.cross((v4 - v1), (v2 - v1)))
    norm_4 = tuple(np.cross((v2 - v1), (v3 - v1)))

    normals = np.array([
        norm_1 * 3,
        norm_2 * 3,
        norm_3 * 3,
        norm_4 * 3,
    ])

    indices = np.arange(0, 12, dtype='int')

    return vertices, indices, normals


def create_pyramid(dtype='float32') -> Tuple[np.array, np.array, np.array]:
    """ Create regular pyramid geometry with square base with base size and height one.

    Args:
        dtype: Data type of output numpy array.

    Returns:
        Tuple[np.array,np.array,np.array]: Tuple of size 3. First is np array for vertices, second for indices,
        and last for the normals.

    """
    base_height = -0.333333

    tip_vert = np.array((0, 0.666666, 0))
    base_top_right_vert = np.array((0.5, base_height, 0.5))
    base_top_left_vert = np.array((-0.5, base_height, 0.5))
    base_bottom_right_vert = np.array((0.5, base_height, -0.5))
    base_bottom_left_vert = np.array((-0.5, base_height, -0.5))

    vertices = np.array([
        # Bottom
        base_top_right_vert,
        base_top_left_vert,
        base_bottom_left_vert,
        base_bottom_right_vert,

        # Front
        tip_vert,
        base_bottom_right_vert,
        base_bottom_left_vert,

        # Back
        tip_vert,
        base_top_left_vert,
        base_top_right_vert,

        # Right
        tip_vert,
        base_top_right_vert,
        base_bottom_right_vert,

        # Left
        tip_vert,
        base_bottom_left_vert,
        base_top_left_vert,
    ], dtype=dtype)

    norm_back = tuple(np.cross((base_top_left_vert - tip_vert), (base_top_right_vert - tip_vert)))
    norm_front = tuple(np.cross((base_bottom_right_vert - tip_vert), (base_bottom_left_vert - tip_vert)))
    norm_right = tuple(np.cross((base_top_right_vert - tip_vert), (base_bottom_right_vert - tip_vert)))
    norm_left = tuple(np.cross((base_bottom_left_vert - tip_vert), (base_top_left_vert - tip_vert)))

    normals = np.concatenate([
        (0, -1, 0) * 4,  # Bottom
        norm_front * 3,  # Front
        norm_back * 3,  # Back
        norm_right * 3,  # Right
        norm_left * 3  # Left
    ]).flatten()

    bottom_indices = np.array([0, 1, 2, 0, 2, 3])
    indices = np.concatenate([bottom_indices, np.arange(4, 16, dtype='int')])

    return vertices, indices, normals
