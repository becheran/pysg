""" Renders a scene with a tree structure
"""
# TODO remove once api is released
import math
import sys

from pyrr import Vector3

sys.path.append("..")  # Adds higher directory to python modules path.

from pysg.constants import color
from pysg.material import BasicMaterial
from pysg.model_3d import Model3D
from pysg.camera import PerspectiveCamera
from pysg.scene import Scene
from pysg.renderer import GLRenderer
from pysg.geometry import BoxGeometry

from example_qt5_window import Example, run_example


class HierarchyScene(Example):
    def __init__(self):
        width = self.WINDOW_SIZE[0]
        height = self.WINDOW_SIZE[1]
        camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
        scene = Scene(background_color=color.rgb["black"], auto_update=True)
        geometry = BoxGeometry(1, 1, 1)
        red_material = BasicMaterial(color=color.rgb["red"])
        green_material = BasicMaterial(color=color.rgb["green"])
        blue_material = BasicMaterial(color=color.rgb["blue"])
        self.cube_1 = Model3D(geometry, red_material, name="Cube_1")
        self.cube_2 = Model3D(geometry, green_material, name="Cube_2")
        self.cube_3 = Model3D(geometry, blue_material, name="Cube_3")
        self.cube_1.add(self.cube_2)
        self.cube_2.add(self.cube_3)
        self.cube_2.local_position = Vector3([5., 0, 0])
        self.cube_3.local_position = Vector3([0, 3, 0])
        camera.local_position.z += 30
        scene.add(self.cube_1)
        self.renderer = GLRenderer(scene, camera)

    def update(self):
        rot = self.wnd.time * 100
        scale = math.fabs(math.sin(self.wnd.time)) + 1
        self.cube_1.local_euler_angles = Vector3([0, rot, 0])
        self.cube_2.local_euler_angles = Vector3([0, -rot, rot])
        self.cube_1.scale = Vector3([scale, scale, scale])
        self.cube_2.scale = Vector3([scale, scale, scale]) * 0.5
        self.cube_3.scale = Vector3([scale, scale, scale])
        self.renderer.viewport = self.wnd.viewport
        self.renderer.render()


try:
    run_example(HierarchyScene)
except Exception as e:
    print(e)
