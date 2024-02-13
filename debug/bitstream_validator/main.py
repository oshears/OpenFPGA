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

def getPrevPorts(root:IO,outFile,level=0) -> [IO]:

    # print(level*'\t' + root.__str__()) 
    outFile.write(level*'\t' + root.__str__() + '\n')

    if not root.hasPrevIO() and "GPIO_PAD" not in root.name:
        outFile.write(level*'\t' + 'ERROR: REACHED A DEADEND TRACING BACK TO FPGA IN PIN!!!\n')

    prevPorts = []    
    for prevIO in root.prevIO:
        prevPorts += getPrevPorts(prevIO, outFile, level + 1)

    # prevPorts = prevPorts + [root]

    
    return prevPorts

def tracePaths(modules:[str, Module]):
    
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


def reportHasSink(root:IO,outFile):
    
    for nextIO in root.nextIO:
        reportHasSink(nextIO, outFile)

    # if not root.hasNextIO() and ("GPIO_PAD" not in root.name) and (root.direction == "output"):

    # if the port does not have a next and is not a GPIO_PAD, it might be a dead end
    if not root.hasNextIO() and ("GPIO_PAD" not in root.name):
        # check to see if it had something leading to it, otherwise we disqualify it
        if root.hasPrevIO():
            # if it had something leading to it, make sure it wasn't just a wire connections (i.e., it was intentionally routed)
            if not root.previoIsDirect[0]:
                outFile.write(f"{root.prevIO[0]}\n")


def printDeadEnds(modules:[str, Module]):

    fh = open(f"{baseDir}/debug/bitstream_validator/deadEnds.txt","w+")

    for module in modules.values():
        for port in module.io.values():
            # if not port.hasNextIO() and not port.hasPrevIO():
            #     fh.write(f"{port}\n")
            # if port.hasNextIO():
            #     fh.write(f"{port}\n")
            # if port.hasPrevIO():
            #     fh.write(f"{port}\n")
            reportHasSink(port,fh)
    fh.close();

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

    # trace paths from outputs back to their inputs
    tracePaths(modules)

    # print dead ends
    printDeadEnds(modules)
