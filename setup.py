from setuptools import setup, Extension

setup(
    name='python-openctm',
    version='1.0.3',
    description='Python Interface for the OpenCTM File Format',
    long_description='Python Interface for the OpenCTM File Format',
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
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: OS Independent",
    )
)
