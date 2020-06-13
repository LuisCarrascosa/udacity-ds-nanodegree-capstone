from setuptools import setup, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='udacity_capstone_LuisCarrascosa',
    version='1.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LuisCarrascosa/udacity-ds-nanodegree-capstone",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['Flask']
)