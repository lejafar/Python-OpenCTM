from setuptools import setup, Distribution, Extension
import sys

setup(
    name='python-openctm',
    version='1.0.0',
    description='Python Interface for the OpenCTM Library',
    long_description='Python Interface for the OpenCTM Library',
    url='https://github.com/lejafar/python-openctm',
    author='Rafael Hautekiet',
    author_email='rafael.hautekiet@oqton.ai',
    license='zlib License',
    ext_modules=[Extension('_foo', ['stub.cc'])],
    packages=['openctm'],
    package_data={
        'openctm': ['libs/libopenctm.dylib',
                    'libs/libopenctm.so'],
    },
    install_requires=[
          'numpy>=1.14.2',
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: OS Independent",
    )
)
