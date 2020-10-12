""" Renders all 3D objects provided by pysg. """

import math

from example_qt5_window import Example, run_example
from pyrr import Vector3

from pysg.camera import PerspectiveCamera
from pysg.constants import color
from pysg.light import PointLight
from pysg.object_3d import CubeObject3D, PlaneObject3D, IcosahedronObject3D, CircleObject3D, TriangleObject3D, \
    CylinderObject3D, TetrahedralObject3D, PyramidObject3D
from pysg.renderer import GLRenderer
from pysg.scene import Scene


class ObjectsScene(Example):
    def __init__(self):
        width = self.WINDOW_SIZE[0]
        height = self.WINDOW_SIZE[1]
        camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
        scene = Scene(background_color=color.rgb["white"], ambient_light=(0.2, 0.2, 0.2))
        light = PointLight(color=(0.8, 0.8, 0.8))
        light.world_position = Vector3([0, 4, 3])
        scene.add(light)
        line_one_y = 1
        line_two_y = -1
        self.cube = CubeObject3D(1, 1, 1, name="Cube", color=(0.9, 0.5, 0.4))
        self.icosahedron = IcosahedronObject3D(1, name="Icosahedron", color=(0.5, 0.4, 0.9))
        self.plane = PlaneObject3D(1, 1, name="Plane", color=(0.5, 0.9, 0.4))
        self.circle = CircleObject3D(0.7, name="Circle", color=(0.9, 0.9, 0.3))
        self.triangle = TriangleObject3D(1, 1, name="Triangle", color=(0.3, 0.9, 0.9))
        self.cylinder = CylinderObject3D(0.7, 0.4, name="Cylinder", color=(0.9, 0.3, 0.9))
        self.tetrahedral = TetrahedralObject3D(1, name="Tetrahedral", color=(0.3, 0.8, 0.9))
        self.pyramid = PyramidObject3D(1, 1.5, name="Pyramid", color=(0.9, 0.9, 0.2))

        self.cube.local_position = [2, line_one_y, 0]
        self.icosahedron.local_position = [-2, line_one_y, 0]
        self.cylinder.local_position = [0, line_one_y, 0]
        self.tetrahedral.local_position = [4, line_one_y, 0]
        self.pyramid.local_position = [-4, line_one_y, 0]

        self.circle.local_position = [0, line_two_y, 0]
        self.plane.local_position = [-2, line_two_y, 0]
        self.triangle.local_position = [2, line_two_y, 0]

        camera.local_position = Vector3([0, 0, 10])
        camera.local_euler_angles = Vector3([0, 0, 0])
        scene.add(self.cube)
        scene.add(self.plane)
        scene.add(self.icosahedron)
        scene.add(self.circle)
        scene.add(self.triangle)
        scene.add(self.cylinder)
        scene.add(self.tetrahedral)
        scene.add(self.pyramid)
        self.renderer = GLRenderer(scene, camera)

    def update(self):
        rot = self.wnd.time * 100
        self.cube.local_euler_angles = Vector3([rot, rot, 0])
        self.icosahedron.local_euler_angles = Vector3([0, rot, rot])
        self.cylinder.local_euler_angles = Vector3([rot, -rot, 0])
        self.tetrahedral.local_euler_angles = Vector3([rot, rot, 0])
        self.pyramid.local_euler_angles = Vector3([rot, rot, 0])
        self.plane.local_euler_angles = Vector3([-90, rot, math.sin(self.wnd.time) * 45])
        self.circle.local_euler_angles = Vector3([-90, rot, math.sin(self.wnd.time) * 45])
        self.triangle.local_euler_angles = Vector3([-90, rot, math.sin(self.wnd.time) * 45])
        self.renderer.viewport = self.wnd.viewport
        self.renderer.render()


if __name__ == "__main__":
    try:
        run_example(ObjectsScene)
    except Exception as e:
        print(e)
