# Examples
Sample scenes to demonstrate the capabilities of *pysg*.

## Simple Scene

Simple rotating 3D cube.

![SimpleScene](img/simpleScene.png)

## Headless Renderer

Render the same simple scene of a rotating 3D cube, but instead of using a QT5 window the scene will be rendered to an image using the headless renderer.

## Hierarchy Scene
Rotating cubes in a scene hierarchy.

![SimpleScene](img/hierarchyScene.png)


## Dependencies
Additionally depends on *PyQt5* for rendering the scenes to a canvas and *Pillow* for image handling for the headless renderer. 

```
pip install -r requirements.txt
```
