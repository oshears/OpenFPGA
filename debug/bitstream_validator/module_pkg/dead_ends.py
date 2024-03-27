from module_pkg.module_classes import *

from typing import List, Union

def hasSink(root:IO):
    
    for nextIO in root.nextIO:
        if hasSink(nextIO):
            return True
            
    if not root.hasNextIO() and ("GPIO_PAD" in root.name):
        return True
    
    return False

def printMuxPaths(root:IO, outFile, level=1):
    outFile.write(level*"\t" + f"{root}\n")
    for nextIO in root.nextIO:
        printMuxPaths(nextIO, outFile, level + 1)
            
def printDeadEnds(modules:Union[str, Module]):

    fh = open(f"./debug/bitstream_validator/results/deadEnds.txt","w+")

    for module in modules.values():
        # for port in module.io.values():
        for mux in module.nodes:
            # if not port.hasNextIO() and not port.hasPrevIO():
            #     fh.write(f"{port}\n")
            # if port.hasNextIO():
            #     fh.write(f"{port}\n")
            # if port.hasPrevIO():
            #     fh.write(f"{port}\n")
            
            # skip IO Pads
            # reportHasSink(port,fh)
            if mux.hasConfigBits() and mux.muxOutput != None and (not hasSink(mux.muxOutput)):
                fh.write(f"{mux}\n")
                printMuxPaths(mux.muxOutput, fh)
    fh.close();