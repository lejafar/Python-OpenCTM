git clone https://github.com/Danny02/OpenCTM.git openctm_tmp
make -C openctm_tmp -f $1
mkdir openctm/libs
mv openctm_tmp/lib/$2 openctm/libs
