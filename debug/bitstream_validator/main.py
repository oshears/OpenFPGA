from module_pkg.module_classes import *
from module_pkg.fpga_top_parse import *
from module_pkg.map_muxes import *
from module_pkg.parse_verilog_modules import *
from module_pkg.get_bitstream_modules import *
from module_pkg.follow_route import *
from module_pkg.graph_json import *
from module_pkg.trace_paths import *
from module_pkg.dead_ends import *
from module_pkg.display_routes import *
from module_pkg.generate_annotated_bitstream import *


# def hasSinglePathPreceedingMux(root:IO, outFile):
    
#     # does this node have a previous driving IO
#     if root.hasPrevIO():
        
#         # if none of the previous driving IO are direct wire connections 
#         # and if the current port is not part of a "grid_io" module
#         if (True not in root.previoIsDirect) and ("grid_io" not in root.moduleName):
            
#             # for each prevIO that is presumably a MUX
#             for prevIO in root.prevIO:
                
#                 # if the mux has multiple options, then it could just be driving something else
#                 # if the mux has one option, then it must be driving this chain
#                 if len(prevIO.nextIO) == 1:
                    
#                     outFile.write(f"\tPossible Single Path Preceeding Mux: {prevIO}\n")
                    
#             return True
#         else:
#             for prevIO in root.prevIO:
#                 return hasSinglePathPreceedingMux(prevIO,outFile)
#     else:
#         return False

# def reportHasSink(root:IO,outFile,pathLength=0):
    
#     for nextIO in root.nextIO:
#         reportHasSink(nextIO, outFile, pathLength + 1)

#     # if not root.hasNextIO() and ("GPIO_PAD" not in root.name) and (root.direction == "output"):

#     # if the port does not have a next and is not a GPIO_PAD, it might be a dead end
#     if not root.hasNextIO() and ("GPIO_PAD" not in root.name):
#         # check to see if it had something leading to it, otherwise we disqualify it
#         # if root.hasPrevIO():
#         # if it had something leading to it, make sure it wasn't just a wire connections (i.e., it was intentionally routed)
#         # if not root.previoIsDirect[0]:
        
#         if "grid_clb" not in root.prevIO[0].moduleName: # TODO: DEBUG: Remove when finished implementing CLB stuff
#             if hasSinglePathPreceedingMux(root, outFile):
#                 outFile.write(f"L={pathLength}, {root.prevIO[0]}\n")


if __name__ == "__main__":

    baseDir = "/home/oshears/Documents/openfpga/OpenFPGA"
    # resultsPath = f"{baseDir}/openfpga_flow/tasks/basic_tests/0_debug_task/random_designs/run003/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
    resultsPath = f"{baseDir}/openfpga_flow/tasks/basic_tests/0_debug_task/design_analysis/latest/k4_N4_tileable_40nm_new/fpga_design/MIN_ROUTE_CHAN_WIDTH"
    bitstreamFile = f"{resultsPath}/fabric_independent_bitstream.xml"

    modules:dict[str, Module] = getModules(baseDir, bitstreamFile)

    # Identify all of the modules being used (from the top level, per the information from the bitstream)
    parseModules(baseDir, resultsPath)

    # Use information from the bitstreams to determine the mux configurations, and thus the internal routes being used
    mapMuxes(baseDir, modules)

    # Connect the modules per the information from fpga_top.v
    parseTop(modules, resultsPath)

    # write the routes being actively used out to files
    displayRoutes(modules)

    # trace paths from outputs back to their inputs
    tracePaths(modules)

    # print dead ends
    printDeadEnds(modules)

    # create a .csv file with bit annotations
    genNewBitstreams(modules)

    # follow_route_for(modules)