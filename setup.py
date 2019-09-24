from setuptools import setup, Extension, find_packages
import os

exec(open('openctm/version.py').read())

long_description = ''
if os.path.exists('README.md'):
    with open('README.md', 'r') as f:
        long_description = f.read()

setup(
    name='python-openctm-nightly',
    version=__version__,
    description='Python Interface for the OpenCTM File Format (nightly)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lejafar/python-openctm',
    author='Rafael Hautekiet',
    author_email='rafaelhautekiet@gmail.com',
    license='zlib License',
    packages=find_packages(),
    install_requires=[
          'numpy>=1.14.2',
      ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: OS Independent",
    ]
)
