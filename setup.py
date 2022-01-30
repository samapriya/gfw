import setuptools
from setuptools import find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setuptools.setup(
    name="gfw",
    version="0.0.2",
    packages=find_packages(),
    package_data={"": ["datasets.json"]},
    url="https://github.com/samapriya/gfw",
    install_requires=[
        "requests>=2.26.0",
        "tenacity>=8.0.1",
        "beautifulsoup4>=4.10.0",
        "tabulate>=0.8.9",
    ],
    license="Apache 2.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    author="Samapriya Roy",
    author_email="samapriya.roy@gmail.com",
    description="Simple CLI for Global Fishing Watch Data",
    entry_points={
        "console_scripts": [
            "gfw=gfw.gfw:main",
        ],
    },
)
