from module_pkg.module_classes import *
from module_pkg.fpga_top_parse import *
from module_pkg.map_muxes import *
from module_pkg.parse_verilog_modules import *
from module_pkg.get_bitstream_modules import *
from typing import List, Union

def displayRoutes(modules:Union[str, Module]):
    fh = open(f"{baseDir}/debug/bitstream_validator/outRoutes.txt","w+")
    for modName, mod in modules.items():
        fh.write(f"{modName}\n")
        for io in mod.io.values():
            if io.nextIO != None:
                fh.write(f"\t{io}\n")
    fh.close()

def getPrevPorts(root:IO,outFile,level=0) -> List[IO]:

    # print(level*'\t' + root.__str__()) 
    outFile.write(level*'\t' + root.__str__() + '\n')

    if not root.hasPrevIO() and "GPIO_PAD" not in root.name:
        outFile.write(level*'\t' + 'ERROR: REACHED A DEADEND TRACING BACK TO FPGA IN PIN!!!\n')

    prevPorts = []    
    for prevIO in root.prevIO:
        prevPorts += getPrevPorts(prevIO, outFile, level + 1)

    # prevPorts = prevPorts + [root]

    
    return prevPorts

def tracePaths(modules:Union[str, Module]):
    
    startPorts = []

    # get the FPGA output pins to trace from
    for module in modules.values():
        if "grid_io" in module.name:
            for port in module.io.values():
                if port.direction == "output" and not port.hasNextIO():
                    startPorts.append(port)


    # recursively get the paths to the input pin of the FPGA
    # paths = []

    fh = open(f"{baseDir}/debug/bitstream_validator/tracedPaths.txt","w+")
    for startPort in startPorts:

        paths = getPrevPorts(startPort,fh)

        # for point in path:
        #     print(point)
        # print("========================")
        
        # paths.append(path)
    
    fh.close()


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

    fh = open(f"{baseDir}/debug/bitstream_validator/deadEnds.txt","w+")

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

def genNewBitstreams(modules):
    module_order = [
        "grid_io_bottom_1__0_",
        "grid_io_bottom_2__0_",
        "grid_io_right_3__1_",
        "grid_io_right_3__2_",
        "sb_2__2_",
        "cbx_2__2_",
        "grid_io_top_2__3_",
        "sb_1__2_",
        "cbx_1__2_",
        "grid_io_top_1__3_",
        "sb_0__2_",
        "sb_0__1_",
        "cby_0__2_",
        "grid_io_left_0__2_",
        "sb_0__0_",
        "cby_0__1_",
        "grid_io_left_0__1_",
        "sb_1__0_",
        "cbx_1__0_",
        "cby_1__1_",
        "grid_clb_1__1_",
        "sb_2__0_",
        "cbx_2__0_",
        "cby_2__1_",
        "grid_clb_2__1_",
        "sb_2__1_",
        "cbx_2__1_",
        "cby_2__2_",
        "grid_clb_2__2_",
        "sb_1__1_",
        "cbx_1__1_",
        "cby_1__2_",
        "grid_clb_1__2_"
    ]
    module_order.reverse()

    fh = open("/home/oshears/Documents/openfpga/OpenFPGA/debug/bitstream_validator/out.csv","w+")
    for moduleName in module_order:
        module:Module = modules[moduleName]

        # for mux in module.nodes:
        for muxIdx in range(len(module.nodes)-1,-1,-1):
            mux = module.nodes[muxIdx]
            bitLine = ""
            bitLine += f"{moduleName},"
            bitLine += f"{mux.name},"
            bitLine += f"{mux.type},"
            bitLine += f"{mux.path},"

            # for bitIdx in range(len(mux.values)-1,-1,-1):
            for bitIdx in range(len(mux.values)):

                fh.write(bitLine + f"{mux.values[bitIdx]}\n")
    
    fh.close()

if __name__ == "__main__":

    baseDir = "/home/oshears/Documents/openfpga/OpenFPGA"
    resultsPath = f"{baseDir}/openfpga_flow/tasks/basic_tests/0_debug_task/random_designs/run003/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
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

    genNewBitstreams(modules)