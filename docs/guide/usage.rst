.. _usage:

=====
Usage
=====


.. code-block:: py

    def __init__(self):
        width = self.WINDOW_SIZE[0]
        height = self.WINDOW_SIZE[1]
        self.camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
        scene = Scene(background_color=color.rgb["white"], ambient_light=(0.2, 0.2, 0.2))
        light = PointLight(color=(0.8, 0.8, 0.8))
        light.world_position = Vector3([2, 2, 2])
        scene.add(light)
        self.cube_1 = CubeObject3D(1, 1, 1, name="Cube_1", color=(0.9, 0.5, 0.4))
        self.cube_2 = CubeObject3D(1, 1, 1, name="Cube_2", color=(0.5, 0.9, 0.4))
        self.cube_3 = CubeObject3D(1, 1, 1, name="Cube_3", color=(0.4, 0.5, 0.9))
        self.cube_1.add(self.cube_2)
        self.cube_2.add(self.cube_3)
        self.cube_2.local_position = Vector3([5., 0, 0])
        self.cube_3.local_position = Vector3([0, 3, 0])
        self.camera.local_position = Vector3([0, 0, 30])
        scene.add(self.cube_1)
        self.renderer = GLRenderer(scene, self.camera)

.. toctree::
    :maxdepth: 2