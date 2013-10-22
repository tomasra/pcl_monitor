#!/bin/tcsh -f

set dir=$1

cd $dir

echo "{" >! chain.h 

foreach x ( `ls Chunk*/*.root -1` )
#echo ${PWD}/${x}
echo 'DTSegmentTree.Add("'${PWD}/${x}'");' >> chain.h
end

echo "}" >> chain.h

