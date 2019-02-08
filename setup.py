import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

if os.environ.get('CI'):
    if os.environ.get('CI_COMMIT_TAG'):
        version = os.environ['CI_COMMIT_TAG']
    else:
        version = os.environ['CI_JOB_ID']
    with open(os.path.join(mypackage_root_dir, 'VERSION'),'a') as version_file:
        version_file.write(str(version))
        
with open(os.path.join(mypackage_root_dir, 'VERSION')) as version_file:
    version = version_file.read().strip()

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
