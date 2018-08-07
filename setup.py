from setuptools import setup, Distribution
import sys

class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True

setup(
    name='python-ctm',
    version='1.0.2',
    description='Python bindings for the OpenCTM Library',
    long_description='Python bindings for the OpenCTM Library',
    url='https://github.com/lejafar/python-ctm',
    author='Rafael Hautekiet',
    author_email='rafael.hautekiet@oqton.ai',
    license='zlib License',
    packages=['openctm'],
    package_data={
        'openctm': ['libopenctm.dylib'],
    },
    install_requires=[
          'numpy>=1.14.2',
      ],
    distclass=BinaryDistribution,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: MacOS",
    )
)
