#!/bin/bash

for i in {1..20}; do
    time for j in {1..100}; do python main.py -safe -t >/dev/null; done
done