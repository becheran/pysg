""" Renders a simple cube without the QT5 window.
Use ModernGL standalone context instead.
"""
# TODO remove once api is released
import sys

from PIL import Image
from pyrr import Vector3

sys.path.append("..")  # Adds higher directory to python modules path.

from pysg.constants import color
from pysg.material import BasicMaterial
from pysg.model_3d import Model3D
from pysg.camera import PerspectiveCamera
from pysg.scene import Scene
from pysg.renderer import HeadlessGLRenderer
from pysg.geometry import BoxGeometry

width = 800
height = 600
camera = PerspectiveCamera(fov=45, aspect=width / height, near=0.01, far=1000)
scene = Scene(background_color=color.rgb["black"], auto_update=True)
geometry = BoxGeometry(1, 1, 1)
material = BasicMaterial(color=color.rgb['red'])
cube = Model3D(geometry, material)
cube.name = "Cube_1"
camera.local_position.z += 5
scene.add(cube)
renderer = HeadlessGLRenderer(scene, camera, width=width, height=height)
cube.local_euler_angles = Vector3([0, 45, 0])
renderer.render()
current_image_data = renderer.current_image()
img = Image.frombytes('RGB', (width, height), current_image_data, 'raw', 'RGB', 0, -1)
img.show()
