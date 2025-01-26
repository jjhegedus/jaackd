from setuptools import setup, find_packages

setup(
    name="jaackd-freecad",
    version="0.1",
    description="Custom functionality for FreeCAD.",
    author="Jeff Hegedus",
    author_email="jeff@22ndtech.com",
    url="https://github.com/jjhegedus/jaackd/jaackd-freecad",
    packages=find_packages(include=["scripts", "scripts.*"]),
    install_requires=[
        "PyQt5",  # Add any additional dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
