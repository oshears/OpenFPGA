import os
from xml.etree import ElementTree

# module_order = [
#     "grid_io_bottom_1__0_",
#     "grid_io_bottom_2__0_",
#     "grid_io_right_3__1_",
#     "grid_io_right_3__2_",
#     "sb_2__2_",
#     "cbx_2__2_",
#     "grid_io_top_2__3_",
#     "sb_1__2_",
#     "cbx_1__2_",
#     "grid_io_top_1__3_",
#     "sb_0__2_",
#     "sb_0__1_",
#     "cby_0__2_",
#     "grid_io_left_0__2_",
#     "sb_0__0_",
#     "cby_0__1_",
#     "grid_io_left_0__1_",
#     "sb_1__0_",
#     "cbx_1__0_",
#     "cby_1__1_",
#     "grid_clb_1__1_",
#     "sb_2__0_",
#     "cbx_2__0_",
#     "cby_2__1_",
#     "grid_clb_2__1_",
#     "sb_2__1_",
#     "cbx_2__1_",
#     "cby_2__2_",
#     "grid_clb_2__2_",
#     "sb_1__1_",
#     "cbx_1__1_",
#     "cby_1__2_",
#     "grid_clb_1__2_"
# ]
# module_order.reverse()

def bitstream_label(module_order, xml_bitstream_filename):
    # suffix = "_16LUT"
    # bitstreamPath = f"../random_bitstreams{suffix}/"

    # files = [f for f in os.listdir(bitstreamPath)]
    # files.sort()

    # for file in files:

    bitstreamPath = "/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/"
    file = "fabric_independent_bitstream.xml"

    # if file[-3:] != "xml":
    #     continue    

    tree = ElementTree.parse(bitstreamPath + file)
    root = tree.getroot()
    

    # iterate through all nodes with a bitstream child
    modules = {}
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

        for bit in bits:
            bitString = ""
            bitString += f"{topModuleName},"
            bitString += f"{nodePath},"
            bitString += f"{nodeName},"
            bitString += f"{bit}\n"
            # fh.write(bitString)

            modules[topModuleName].append(bitString)

    ## write modules and routing nodes out to file
    # fh = open(f"../random_bitstreams{suffix}/{file}.csv","w+")
    fh = open(f"debug/architectures/arch_gen/results/fpga_4x4_clb/_info/_{file}.csv","w+")
    fh.write("module_name,path,name,bit\n")
    for module in module_order:
        for i in range(len(modules[module])-1,-1,-1):
            fh.write(modules[module][i])

    fh.close()


# bitstream = "/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/fabric_independent_bitstream.xml"
# bitstream_label(bitstream)