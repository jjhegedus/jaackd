import debugpy
import os

# Start debugpy and wait for the debugger to attach
debugpy.listen(("localhost", 5678))
print("Waiting for debugger to attach...")
debugpy.wait_for_client()
print("Debugger attached.")

# Run FreeCAD
freecad_bin = r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe"
os.system(f'"{freecad_bin}"')