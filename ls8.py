import sys
from cpu import *

if len(sys.argv) == 2:
    cpu = CPU()
    cpu.load(sys.argv[1]) # Pass File Name to Load
    cpu.run()
else:
    print("Error!: Provide a File Name to Execute this Function.")