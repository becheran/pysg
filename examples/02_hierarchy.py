""" Renders a scene with a tree structure
"""
# TODO remove once api is released
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
        material = BasicMaterial()
        self.cube_1 = Model3D(geometry, material, name = "Cube_1")
        self.cube_2 = Model3D(geometry, material, name = "Cube_2")
        self.cube_3 = Model3D(geometry, material, name = "Cube_3")
        self.cube_1.add(self.cube_2)
        self.cube_2.add(self.cube_3)
        self.cube_2.local_position = Vector3([3., 0, 0])
        self.cube_3.local_position = Vector3([0, 3.0, 0])
        camera.local_position.z += 15
        scene.add(self.cube_1)
        self.renderer = GLRenderer(scene, camera)

    def update(self):
        self.renderer.viewport = self.wnd.viewport
        self.renderer.render()
        rot = self.wnd.time * 100
        self.cube_1.local_euler_angles = Vector3([0, rot, 0])
        self.cube_2.local_euler_angles = Vector3([0, -rot, rot])


try:
    run_example(HierarchyScene)
except Exception as e:
    print(e)
