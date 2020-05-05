import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
from distutils.version import LooseVersion

from setuptools import Extension
from setuptools import setup
from setuptools.command.build_ext import build_ext

exec(open('openctm/version.py').read())

long_description = ''
if os.path.exists('README.md'):
    with open('README.md', 'r') as f:
        long_description = f.read()

class MakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class MakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        project_folder = pathlib.Path(self.get_ext_fullpath(ext.name)).parent
        source_folder = pathlib.Path(ext.sourcedir)

        # pick make based on os
        makename = "make"
        if sys.platform == 'win32':
            makename = "mingw32-make"

        # pick makefille based on os
        makefilename = "Makefile.linux"
        if sys.platform == 'darwin':
            makefilename = "Makefile.macosx"
        if sys.platform == 'win32':
            makefilename = "Makefile.mingw"
        makefile_args = ['-f', makefilename]

        # call make cmd
        make_args = ['-C', str(source_folder)] + makefile_args
        subprocess.check_call([makename] + make_args + ['openctm'], cwd=str(source_folder))

        # copy shared object to where it will be expected
        lib_folder = project_folder / 'openctm/libs'
        lib_folder.mkdir(exist_ok=True)
        for shared_object in (source_folder / 'lib').glob('*openctm.*'):
            shutil.copyfile(str(shared_object), str(lib_folder / shared_object.name))


setup(name='python-openctm',
      version=__version__,
      author='Rafael Hautekiet',
      author_email='rafaelhautekiet@gmail.com',
      license='zlib License',
      description='Python Interface for the OpenCTM File Format',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/lejafar/python-openctm',
      ext_modules=[MakeExtension('openctm', 'submodules/OpenCTM')],
      cmdclass=dict(build_ext=MakeBuild),
      zip_safe=False,
      packages=['openctm'],
      package_data={'openctm': ['libs/*']},
      install_requires=['numpy'],
      classifiers=[
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Natural Language :: English",
          "Topic :: Scientific/Engineering",
          "License :: OSI Approved :: zlib/libpng License",
          "Operating System :: OS Independent",
      ])
