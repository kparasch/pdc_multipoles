#!/bin/bash

for order in $(seq 3 20);
do	
    for KL in -1e8 -1e7 -1e6 -1e5 -1e4 -1e3 -1e2 -1e1 -0 1e1 1e2 1e3 1e4 1e5 1e6 1e7 1e8;
    do
        sbatch job.sh 3 $KL --skew
    done
done

