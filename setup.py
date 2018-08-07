from setuptools import setup, Distribution
import sys

class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True

setup(
    name='python-openctm',
    version='1.0.0',
    description='Python Interface for the OpenCTM Library',
    long_description='Python Interface for the OpenCTM Library',
    url='https://github.com/lejafar/python-openctm',
    author='Rafael Hautekiet',
    author_email='rafael.hautekiet@oqton.ai',
    license='zlib License',
    packages=['openctm'],
    package_data={
        'openctm': ['libs/libopenctm.dylib',
                    'libs/libopenctm.so'],
    },
    install_requires=[
          'numpy>=1.14.2',
      ],
    distclass=BinaryDistribution,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    )
)
