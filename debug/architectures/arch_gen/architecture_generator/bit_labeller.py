import os
from xml.etree import ElementTree

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