import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()
    
if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setuptools.setup(
    name="pysg",
    version=version,
    author="Armin Becher",
    author_email="becherarmin@gmail.com",
    description="Simple and lightweight 3D render scene graph for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/becheran/pysg",
    packages=setuptools.find_packages(),
    # Python 3.6 required minimum due to the use of static type checking
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
