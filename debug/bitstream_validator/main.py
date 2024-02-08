from module_pkg.module_classes import *
from module_pkg.fpga_top_parse import *
from module_pkg.module_graph import *

def displayRoutes(modules:[str, Module]):
    fh = open(f"{baseDir}/debug/bitstream_validator/outRoutes.txt","w+")
    for modName, mod in modules.items():
        fh.write(f"{modName}\n")
        for io in mod.io.values():
            if io.nextIO != None:
                fh.write(f"\t{io}\n")
    fh.close()

if __name__ == "__main__":
    modules:dict[str, Module] = getModules()

    # Identify all of the modules being used (from the top level, per the information from the bitstream)
    parseModules()

    # Use information from the bitstreams to determine the mux configurations, and thus the internal routes being used
    mapMuxes(modules)
    
    # Connect the modules per the information from fpga_top.v
    parseTop(modules)

    # write the routes being actively used out to files
    displayRoutes(modules)
