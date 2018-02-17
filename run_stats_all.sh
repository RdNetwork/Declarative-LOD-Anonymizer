#!/bin/bash

readonly PMAX=4
readonly UMAX=4

echo "Starting stats generation for [P=[1,4],U=[1,4]..."

for p in $(seq 1 $PMAX)
do
    for u in $(seq 1 $UMAX)
    do
        echo "P=$p / U=$u"
        python main.py $p $u -s
    done
done