""" Renders a scene with a tree structure
"""
# TODO remove once api is released
import math
import sys

from pyrr import Vector3

from pysg.light import PointLight

sys.path.append("..")  # Adds higher directory to python modules path.

from pysg.constants import color
from pysg.object_3d import CubeObject3D, PlaneObject3D, IcosahedronObject3D, CircleObject3D, TriangleObject3D, \
    CylinderObject3D
from pysg.camera import PerspectiveCamera
from pysg.scene import Scene
from pysg.renderer import GLRenderer

from example_qt5_window import Example, run_example


class HierarchyScene(Example):
    def __init__(self):
        width = self.WINDOW_SIZE[0]
        height = self.WINDOW_SIZE[1]
        camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
        scene = Scene(background_color=color.rgb["white"], ambient_light=(0.2, 0.2, 0.2))
        light = PointLight(color=(0.8, 0.8, 0.8))
        light.world_position = Vector3([0, 4, 3])
        scene.add(light)
        self.cube = CubeObject3D(1, 1, 1, name="Cube", color=(0.9, 0.5, 0.4))
        self.icosahedron = IcosahedronObject3D(1, name="Icosahedron", color=(0.5, 0.4, 0.9))
        self.plane = PlaneObject3D(1, 1, name="Plane", color=(0.5, 0.9, 0.4))
        self.circle = CircleObject3D(0.7, name="Circle", color=(0.9, 0.9, 0.3))
        self.triangle = TriangleObject3D(1, 1, name="Triangle", color=(0.3, 0.9, 0.9))
        self.cylinder = CylinderObject3D(0.7, 0.4, name="Cylinder", color=(0.9, 0.3, 0.9))
        self.circle.local_position = [0, -2, 0]
        self.plane.local_position = [-2, -2, 0]
        self.triangle.local_position = [2, -2, 0]
        self.cube.local_position = [2, 0, 0]
        self.icosahedron.local_position = [-2, 0, 0]
        self.cylinder.local_position = [0, 0, 0]
        camera.local_position = Vector3([0, 1, 10])
        camera.local_euler_angles = Vector3([10, 0, 0])
        scene.add(self.cube)
        scene.add(self.plane)
        scene.add(self.icosahedron)
        scene.add(self.circle)
        scene.add(self.triangle)
        scene.add(self.cylinder)
        self.renderer = GLRenderer(scene, camera)

    def update(self):
        rot = self.wnd.time * 100
        self.cube.local_euler_angles = Vector3([rot, rot, 0])
        self.icosahedron.local_euler_angles = Vector3([0, rot, rot])
        self.cylinder.local_euler_angles = Vector3([rot, -rot, 0])
        self.plane.local_euler_angles = Vector3([-90, rot, math.sin(self.wnd.time) * 45])
        self.circle.local_euler_angles = Vector3([-90, rot, math.sin(self.wnd.time) * 45])
        self.triangle.local_euler_angles = Vector3([-90, rot, math.sin(self.wnd.time) * 45])
        self.renderer.viewport = self.wnd.viewport
        self.renderer.render()


try:
    run_example(HierarchyScene)
except Exception as e:
    print(e)
