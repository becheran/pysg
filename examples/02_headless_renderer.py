""" Renders a simple cube without the QT5 window.
Use ModernGL standalone context instead.
"""
# TODO remove once api is released
import sys

from PIL import Image
from pyrr import Vector3

from pysg.light import PointLight

sys.path.append("..")  # Adds higher directory to python modules path.

from pysg.constants import color
from pysg.object_3d import Object3D, BoxObject3D
from pysg.camera import PerspectiveCamera
from pysg.scene import Scene
from pysg.renderer import HeadlessGLRenderer

width = 800
height = 600
camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
scene = Scene(background_color=color.rgb["black"], ambient_light=(0.2, 0.2, 0.2))
light = PointLight(color=(0.8, 0.8, 0.8))
light.world_position = Vector3([1, 1, 1])
scene.add(light)
cube = BoxObject3D(1, 1, 1, color=color.rgb["red"])
cube.name = "Cube_1"
camera.local_position += Vector3([0, 0, 5])
scene.add(cube)
renderer = HeadlessGLRenderer(scene, camera, width=width, height=height)
cube.local_euler_angles = Vector3([0, 45, 0])
renderer.render()
current_image_data = renderer.current_image()
img = Image.frombytes('RGB', (width, height), current_image_data, 'raw', 'RGB', 0, -1)
img.show()
