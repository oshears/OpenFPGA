from module_pkg import *
from module_pkg.module_classes import *
from typing import List, Union

import json

def getPrevPorts(root:IO, outFile, level=0, paths_dict=None, index=[0,0], path_option = 0) -> List[IO]:

    # add this to the dictionary if it isn't already there
    paths_dict["nodes"].append({
        "index":index[0], 
        "name":root.getFullName(), 
        "module":root.moduleName, 
        "mux": "None" if root.mux == None else root.mux.name, 
        "group":module_order.index(root.moduleName),
        "level":level,
        "output":index[1],
        "path_direction":path_option # TODO: what should the final axis be?
        })
    current_index = index[0]

    # print(level*'\t' + root.__str__()) 
    outFile.write(level*'\t' + f"{index[0]}: " + root.__str__() + '\n')

    if not root.hasPrevIO() and "GPIO_PAD" not in root.name:
        outFile.write(level*'\t' + 'ERROR: REACHED A DEADEND TRACING BACK TO FPGA IN PIN!!!\n')

    prevPorts:List[IO] = []    
    for prevIO in root.prevIO:
        index[0] += 1
        paths_dict["links"].append([current_index,index[0]])
        prevPorts += getPrevPorts(prevIO, outFile, level + 1, paths_dict=paths_dict, index=index, path_option=path_option)
        path_option += 1

    # prevPorts = prevPorts + [root]

    
    return prevPorts

def tracePaths(modules:Union[str, Module]):
    
    startPorts:List[IO] = []

    # get the FPGA output pins to trace from
    for module in modules.values():
        if "grid_io" in module.name:
            for port in module.io.values():
                if port.direction == "output" and not port.hasNextIO():
                    startPorts.append(port)


    # recursively get the paths to the input pin of the FPGA
    # paths = []

    fh = open(f"./debug/bitstream_validator/results/tracedPaths.txt","w+")
    paths_fh = open(f"./debug/bitstream_validator/results/tracedPaths.json","w+")
    paths_dict = {"nodes":[],"links":[]}
    index = [0,0]
    for startPort in startPorts:
        paths = getPrevPorts(startPort,fh,paths_dict=paths_dict,index=index)
        index[1] += 1

        # for point in path:
        #     print(point)
        # print("========================")
        
        # paths.append(path)
    
    paths_fh.write(json.JSONEncoder().encode(paths_dict))
    paths_fh.close()
    
    fh.close()