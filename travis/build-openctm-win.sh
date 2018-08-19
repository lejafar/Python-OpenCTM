# ./build-openctm-win.sh

git clone https://github.com/Danny02/OpenCTM.git openctm_tmp
mingw32-make -f Makefile.mingw
mkdir openctm/libs
mv openctm_tmp/lib/libopenctm.dll openctm/libs
