import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wzk",
    version="0.1.2",
    author="zhaokai wang",
    author_email="self@wzk.plus",
    description="wzk's library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wzk1015/wzk-pypi-package",
    packages=setuptools.find_packages()
)
