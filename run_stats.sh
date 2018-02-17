#!/bin/bash

echo "Starting stats generation for [P=3,U=3]..."
python main.py 3 3 -s
python main.py 3 3 -hu
python main.py 3 3 -hp
