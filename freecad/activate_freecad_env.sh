#!/bin/bash

# Path to FreeCAD libraries
#export FREECAD_LIB_PATH=/usr/lib/freecad-daily-python3/lib
export FREECAD_LIB_PATH=/usr/lib/freecad-daily/lib

# Activate the virtual environment
source .venv/bin/activate

# Set PYTHONPATH to include FreeCAD libraries
export PYTHONPATH=$FREECAD_LIB_PATH:$PYTHONPATH

echo "FreeCAD environment activated."