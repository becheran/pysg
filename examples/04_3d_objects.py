""" Renders a scene with a tree structure
"""
# TODO remove once api is released
import math
import sys

from pyrr import Vector3

from pysg.light import PointLight

sys.path.append("..")  # Adds higher directory to python modules path.

from pysg.constants import color
from pysg.object_3d import BoxObject3D, PlaneObject3D, IcosahedronObject3D
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
        light.world_position = Vector3([2, 2, 3])
        scene.add(light)
        self.cube_1 = BoxObject3D(1, 1, 1, name="Cube_1", color=(0.9, 0.5, 0.4))
        self.plane_1 = PlaneObject3D(1, 1, name="Plane_1", color=(0.5, 0.9, 0.4))
        self.icosahedron_1 = IcosahedronObject3D(1, name="Icosahedron_1", color=(0.5, 0.4, 0.9))
        self.cube_1.local_position = [2, 0, 0]
        self.icosahedron_1.local_position = [-2, 0, 0]
        camera.local_position = Vector3([0, 1, 10])
        camera.local_euler_angles = Vector3([10, 0, 0])
        scene.add(self.cube_1)
        scene.add(self.plane_1)
        scene.add(self.icosahedron_1)
        self.renderer = GLRenderer(scene, camera)

    def update(self):
        rot = self.wnd.time * 100
        self.cube_1.local_euler_angles = Vector3([rot, rot, 0])
        self.plane_1.local_euler_angles = Vector3([-90, rot, math.sin(self.wnd.time) * 45])
        self.icosahedron_1.local_euler_angles = Vector3([0, rot, rot])
        self.renderer.viewport = self.wnd.viewport
        self.renderer.render()


try:
    run_example(HierarchyScene)
except Exception as e:
    print(e)
