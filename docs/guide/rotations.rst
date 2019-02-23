.. _rotations:
=============================
Rotations & Coordinate System
=============================
For *pysg* a right handed coordinate system is used.
The x-axis is facing right, the y-axis up, and the z-axis to the front.
The *pysg* library uses ModernGL_ to render all 3D objects in the scene.
The camera inside a scene is facing towards the -z direction.

.. _ModernGL: https://github.com/cprogrammer1994/ModernGL

For the *pysg* scene graph all rotations are internally represented as quaternions.
If the rotation of an object is set via Euler angles they are converted to quaternions.
For the Euler angles the rotation order is YZX.

.. seealso::
    The website EuclideanSpace_ contains more information about rotations and how they
    are implemented in *pysg*.

.. _EuclideanSpace: https://www.euclideanspace.com/

.. toctree::
    :maxdepth: 1