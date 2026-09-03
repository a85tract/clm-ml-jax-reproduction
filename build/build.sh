#!/bin/bash
# Build the CLM-ml_v2.CHATS offline executable with gfortran -O2 in topological
# USE order (output/topo_order.txt, from stage.py). The upstream tree is read,
# never modified. Run from build/: ./build.sh, then cd run && ../prgm.exe < nl.CHATS7.05.2007
# The namelist is upstream's, with its input paths pointed at the clone and
# its output at ./out/ -- the same rewrite record.py makes for the recorder.
set -e
U=../upstream
NF=$(nf-config --prefix)
FC="gfortran -O2 -ffree-line-length-none -fno-range-check -I$NF/include"
mkdir -p obj run/out
for m in $(cat ../output/topo_order.txt); do
  f=$(find $U -iname "$m.F90" | head -1)
  [ -z "$f" ] && { echo "no file for $m"; exit 1; }
  $FC -c -J obj -o obj/$m.o $f
done
$FC -o prgm.exe obj/*.o -L$NF/lib -lnetcdff -L$(nc-config --libdir) -lnetcdf
sed -e "s#'\.\./input_files#'../../upstream/input_files#" -e "s#dirout *= *'[^']*'#dirout           = './out/'#" \
  $U/offline_executable/nl.CHATS7.05.2007 > run/nl.CHATS7.05.2007
echo BUILT; ls -la prgm.exe
