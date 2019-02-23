.. _usage:

=====
Usage
=====
With *pysg* it is possible to create simple scenes with basic 3D geometries and render them to screen
or save them as images on the hard drive.

The example described in this section only render a single image and display it on the screen using
pillow_.

.. _pillow: https://pypi.org/project/Pillow/

.. seealso::

    More examples in the example folder:
    https://gitlab.com/becheran/pysg/tree/master/examples

References
==========
Load all required references. The pillow_ (PIL) library is required to display the result
image of the standalone renderer. The pyrr_ vector is needed to define a new position for
the 3D elements in the scene.

.. _pyrr: https://github.com/adamlwgriffiths/Pyrr

.. code-block:: py

    from PIL import Image
    from pyrr import Vector3
    import pysg

Init
====
Initialize all camera, scene, and renderer. All three things are required to display a 3D scene.
The camera defines the viewing volume within an scene. The scene is the root element of all 3D objects
which are used for rendering. A scene also defines the ambient brightness and background color.
The renderer is used to actually synthesise the described *pysg* scene. It can either
be a standalone renderer, rendering to a texture which can later be saved as an image. With
the  GLRenderer the scene can be displayed within a OpenGL windows.

.. code-block:: py

    # Constants. Width and height of image.
    WIDTH = 800
    HEIGHT = 600
    # Camera, scene and renderer is always needed to render a 3D scene.
    camera = pysg.PerspectiveCamera(fov=45, aspect=800 / 600, near=0.01, far=1000)
    scene = pysg.Scene(background_color=(1, 1, 1), ambient_light=(0.2, 0.2, 0.2))
    renderer = pysg.HeadlessGLRenderer(scene, camera, width=WIDTH, height=HEIGHT)

Scene
=====
The scene in *pysg* contains all objects with their 3D transform which describe a renderable 3D
scenario. Lighting is also handles within a scene.

.. code-block:: py

    # Change position of camera to view whole scene (camera is looking towards -z).
    camera.local_position += Vector3([0, 0, 10])
    # Add point-light to scene and define color as white. With ambient color sum of brightness is 1.
    light = pysg.PointLight(color=(0.8, 0.8, 0.8))
    # Change position of light in scene.
    light.world_position = Vector3([1, 1, 1])
    # Add cube object with 1x1x1 size and blueish color.
    cube = pysg.CubeObject3D(1, 1, 1, color=(0.4, 0.5, 0.9))
    # Rotate cube so that not the only the a corner is now in front of camera.
    cube.local_euler_angles = Vector3([0, 45, 0])
    # Add 3D elements to scene.
    scene.add(cube)
    scene.add(light)

Render
======
Rendering is the last step of the *pysg* pipeline. If object transforms or properties are updated,
the render function can be called within a loop in order to simulate dynamic scene changes.

.. code-block:: py

    # Actually render the 3D scene.
    renderer.render()
    # Get current rendering from texture as byte array.
    current_image_data = renderer.current_image()
    # Convert byte array to pillow image and use show function to display it.
    img = Image.frombytes('RGB', (WIDTH, HEIGHT), current_image_data, 'raw', 'RGB', 0, -1)
    img.show()

.. toctree::
    :maxdepth: 2