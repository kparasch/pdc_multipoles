#!/bin/bash

for ii in 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.5 3 3.5 4 4.5 5 5 6 6.5 7 7.5 8 8.5 9 9.5 10;
do
    echo "Running with scale $ii"
    python 003_da_with_specs.py --scale $ii
done