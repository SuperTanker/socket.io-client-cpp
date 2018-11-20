import sys
from setuptools import setup

if sys.version_info.major < 3:
    sys.exit("Error: Please upgrade to Python3")


setup(
    name="socketioclientcpp",
    version="0.1.0",
    author="tech@tanker.io",
    install_requires=["ci"],
    extras_require={"dev": []},
)
