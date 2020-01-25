import setuptools
import os

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

dirname = os.path.dirname(__file__)

with open('pysg/version.py', 'r') as f:
    exec(f.read())

setuptools.setup(
    name="pysg",
    version=__version__,
    author="Armin Becher",
    author_email="becherarmin@gmail.com",
    description="Simple and lightweight 3D render scene graph for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/becheran/pysg",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    license='MIT',
    install_requires=[
        'moderngl>=5.4.2,<6',
        'numpy>=1.15.4,<2',
        'pyrr>=0.10.0<1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
