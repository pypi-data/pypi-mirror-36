# coding=utf-8
import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bendercoder",
    version="1.1",
    author="Manolis Tsoukalas",
    author_email="emmtsoukalas@gmail.com",
    description="Library for encoding and decoding bencode data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m19t12/bendercoder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
