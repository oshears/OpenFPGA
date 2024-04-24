from module_pkg.module_classes import *

from typing import List, Union


def genNewBitstreams(modules:Union[str, Module], module_order, window=None, out_filename="out.csv"):
    
    bitCount = 0

    fh = open(f"/home/oshears/Documents/openfpga/OpenFPGA/debug/bitstream_validator/results/{out_filename}","w+")

    fh.write("bit index,bit value,module,name,type,path,description,sinks\n")

    for moduleName in module_order:
        if window is None or moduleName in window:
            module:Module = modules[moduleName]

            # for mux in module.nodes:
            for muxIdx in range(len(module.nodes)-1,-1,-1):
                mux:RoutingNode = module.nodes[muxIdx]
                bitLine = ""
                bitLine += f"{moduleName},"
                bitLine += f"{mux.name},"
                bitLine += f"{mux.type},"
                bitLine += f"{mux.path},"
                bitLine += f"{mux.desc},"

                # for bitIdx in range(len(mux.values)-1,-1,-1):
                for bitIdx in range(len(mux.values)):
                    
                    # this tells us where the results of this mux go (sinks)
                    # tells us what (sinks) does this mux drive
                    muxDrives = ",".join(mux.sinks) if mux.sinks is not None else "not specified"

                    fh.write(f"{bitCount}," + f"{mux.values[bitIdx]}," + bitLine + f"{muxDrives}" + "\n")

                    bitCount += 1
    
    fh.close()