.. _rotations:
=============================
Rotations & Coordinate System
=============================
For *pysg* a right handed coordinate system is used.
The x-axis is facing right, the y-axis up, and the z-axis to the front.
The *pysg* library uses ModernGL to render all 3D objects in the scene.
The camera inside a scene is facing towards the -z direction.

For the *pysg* scene graph all rotations are internally represented as quaternions.
If rotation is set via euler angles they are converted to quaternions. For the euler
angles the rotation order is YZX.

Also see EuclideanSpace_ website for more information about rotations.

.. _EuclideanSpace: https://www.euclideanspace.com/

.. toctree::
    :maxdepth: 1