#!/bin/tcsh -f
foreach x (*Chunk*) 
 cd $x
 bsub -q 8nh < ./batchScript.sh
# bsub -q 1nd < ./batchScript.sh
 cd -
end
