import os
from typing import List
from xml.etree import ElementTree
import math
import re

def bitstream_label(module_order, xml_bitstream_filename):
    # suffix = "_16LUT"
    # bitstreamPath = f"../random_bitstreams{suffix}/"

    # files = [f for f in os.listdir(bitstreamPath)]
    # files.sort()

    # for file in files:

    # bitstreamPath = "/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/"
    # file = "fabric_independent_bitstream.xml"

    # if file[-3:] != "xml":
    #     continue    

    tree = ElementTree.parse(xml_bitstream_filename)
    root = tree.getroot()
    

    # iterate through all nodes with a bitstream child
    modules = {}
    module_info = {}
    for configNode in root.findall(".//bitstream/.."): 
        topModuleName = configNode[0][1].attrib["name"]
        nodePath = "/".join([f"{configNode[0][i].attrib['name']}" for i in range(1,len(configNode[0]))])
        nodeName = configNode[0][-1].attrib["name"]
        bits = None

        # if "grid_clb" in topModuleName:
        bits = [int(configNode[-1][i].attrib["value"]) for i in range(len(configNode[-1]))]
        # else:
        #     bits = [int(configNode[-1][i].attrib["value"]) for i in range(len(configNode[-1])-1,-1,-1)]


        if topModuleName not in modules.keys():
            modules[topModuleName] = []
            module_info[topModuleName] = []

        for bit in bits:
            bitString = ""
            bitString += f"{topModuleName},"
            bitString += f"{nodePath},"
            bitString += f"{nodeName},"
            bitString += f"{bit}\n"
            # fh.write(bitString)

            modules[topModuleName].append(bitString)

            bit_info = {
                "module name": topModuleName,
                "node path": nodePath,
                "node name": nodeName,
                "bit value": bit
            }
            module_info[topModuleName].append(bit_info)

    ## write modules and routing nodes out to file
    # fh = open(f"../random_bitstreams{suffix}/{file}.csv","w+")
    fh = open(f"debug/architectures/arch_gen/results/fpga_4x4_clb/_info/bit_labels.csv","w+")
    fh.write("module_name,path,name,bit\n")
    for module in module_order:
        for i in range(len(modules[module])-1,-1,-1):
            fh.write(modules[module][i])

    fh.close()

    return module_info

# bitstream = "/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/fabric_independent_bitstream.xml"
# bitstream_label(bitstream)

def device_visualization(module_info, module_config_order:List=None):
    device_width = int(math.sqrt(len(module_info) - 4*4))
    # print(device_width)

    # locations = [ [None] * device_width] * device_width
    locations = []
    for x in range(device_width):
        locations.append([])
        for y in range(device_width):
            locations[x].append(None)

    for module_name in module_info.keys():

        if 'grid_io' in module_name:
            continue

        if x := re.search('sb_(\d+)__(\d+)_',module_name):
            sb_x = int(x.group(1))
            sb_y = int(x.group(2))

            locations[sb_x * 2][sb_y * 2] = module_name
        
        if x := re.search('grid_clb_(\d+)__(\d+)_',module_name):
            clb_x = int(x.group(1))
            clb_y = int(x.group(2))

            locations[clb_x * 2 - 1][clb_y * 2 - 1] = module_name
        
        if x := re.search('cbx_(\d+)__(\d+)_',module_name):
            cbx_x = int(x.group(1))
            cbx_y = int(x.group(2))

            locations[cbx_x * 2 - 1][cbx_y * 2] = module_name
        
        if x := re.search('cby_(\d+)__(\d+)_',module_name):
            cby_x = int(x.group(1))
            cby_y = int(x.group(2))

            locations[cby_x * 2][cby_y * 2 - 1] = module_name

    # print module names
    print("Module Arrangement")
    for y in range(device_width-1,-1,-1):
        for x in range(device_width):
            module_name = locations[x][y]
            print(f"{locations[x][y]},",end="")
            # print(f"\t| {locations[x][y]}",end="")
        print("")

    # print configuration order
    print("Configuration Order")
    for y in range(device_width-1,-1,-1):
        for x in range(device_width):
            module_name = locations[x][y]
            config_index = module_config_order.index(module_name)
            print(f"{config_index},",end="")
            # print(f"\t| {locations[x][y]}",end="")
        print("")

    # print bit counts
    print("Bit Counts:")
    for y in range(device_width-1,-1,-1):
        for x in range(device_width):
            module_name = locations[x][y]
            print(f"{len(module_info[module_name])},",end="")
            # print(f"\t| {locations[x][y]}",end="")
        print("")