# -*- coding: utf-8 -*-
""" Create basic geometries which are used to create buffered primitives in vRAM."""
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
        (width, height, depth,),
        # top left
        (-width, height, depth,),
        # bottom left
        (-width, -height, depth,),
        # bottom right
        (width, -height, depth,),

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
