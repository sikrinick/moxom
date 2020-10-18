from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="moxom",
    version="1.0.0",
    author="Mykyta Sikriier",
    author_email="sikrinick@gmail.com",
    description="Library to build simple user-friendly CLI API for your Python scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sikrinick/moxom",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)