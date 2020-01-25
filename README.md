![header](https://gitlab.com/becheran/pysg/raw/master/_img/header.png)
# pysg

Simple and lightweight 3D render scene graph for python 3 (tested with 3.8).

## Installation
Install the latest version of pysg via pip:

	pip install pysg 

## Documentation

[Link documentation](https://pysg.readthedocs.io/en/latest/).


## Examples

Checkout the [examples folder](/examples).

## Dependencies

* [ModernGL](https://github.com/cprogrammer1994/ModernGL) - OpenGL related stuff.
* [pyrr](https://github.com/adamlwgriffiths/Pyrr) - Math operations in 3D like matrix multiplication etc.. Fast due to the heavy use of [numpy](http://www.numpy.org/).

## Built With

* [SPHINX](http://www.sphinx-doc.org/en/master/) - Used to generate Documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments
Many thanks to the [ModernGL](https://github.com/cprogrammer1994/ModernGL) and [pyrr](https://github.com/adamlwgriffiths/Pyrr) teams. 

Also many thanks to the [three.js](https://threejs.org/) developers where I got a lot of inspiration from.

## TODO

- [ ] Improve render performance (use multi instance rendering)
- [ ] Allow more light sources and add different light types