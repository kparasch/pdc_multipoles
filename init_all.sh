#!/bin/bash

mkdir simulations -p
for i in $(seq 1 20);
do
    python 000_init_df.py --folder simulations --order $i
    python 000_init_df.py --folder simulations --order $i --skew
done
