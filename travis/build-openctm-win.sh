# ./build-openctm-win.sh

git clone https://github.com/Danny02/OpenCTM.git openctm_tmp
nmake /f Makefile.msvc
mkdir openctm/libs
mv openctm_tmp/lib/libopenctm.dll openctm/libs
