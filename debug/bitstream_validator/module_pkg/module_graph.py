from . import *
# from module_classes import *
# import module_pkg.module_classes.Module
from .module_classes import *


### Tasks
    
### 1. Make graph connecting each node
    
### get modules and their bit configurations
def getModules() -> dict[str, Module]:
    print(bitstreamFile)
    tree = ElementTree.parse(bitstreamFile)
    root = tree.getroot()

    modules = {}
    for child in root:
        moduleName = child.attrib['name']

        if "clb" in moduleName: 
            modules[moduleName] = CLBModule(child.attrib['name'],"")
        else:
            modules[moduleName] = Module(child.attrib['name'],"")
        
    for primitive in root.findall(".//bitstream/.."): # iterate through all nodes with a bitstream child
        path = "/".join([f"{primitive[0][i].attrib['name']}" for i in range(1,len(primitive[0]))])
        topModuleName = primitive[0][1].attrib["name"]
        
        bits = [int(primitive[-1][i].attrib["value"]) for i in range(len(primitive[-1])-1,-1,-1)]
        
        node = RoutingNode(primitive[0][-1].attrib["name"],primitive[0][-1].attrib["name"],path,len(bits),bits)

        modules[topModuleName].addNode(node)
        
    
    ## write modules and routing nodes out to file
    fh = open(f"{baseDir}/debug/bitstream_validator/mux_mappings/bit_configs/fullConfig.bit","w+")
    # fh.write(modules["cbx_1__2_"].__str__())
    for moduleName in module_order:
        # print(module)
        modules[moduleName].nodes.reverse()
        fh.write(modules[moduleName].__str__())
        fh_module = open(f"{baseDir}/debug/bitstream_validator/mux_mappings/bit_configs/{moduleName}.bit","w+")
        fh_module.write(modules[moduleName].__str__())
        fh_module.close()
    fh.close()

    return modules


### get muxes and io, and map them to the modules
def mapMuxes(modules:dict[str,Module]):

    # moduleName = "sb_0__0_"
    # moduleName = "cbx_1__2_"

    module_mappings = {
        # "grid_io_top_1__3_":"grid_io_top",
        # "grid_io_top_2__3_":"grid_io_top",
        # "grid_io_right_3__2_":"grid_io_right",
        # "grid_io_right_3__1_":"grid_io_right",
        # "grid_io_bottom_2__0_":"grid_io_bottom",
        # "grid_io_bottom_1__0_":"grid_io_bottom",
        # "grid_io_left_0__1_":"grid_io_left",
        # "grid_io_left_0__2_":"grid_io_left",
        "grid_clb_1__1_":"logical_tile_clb_mode_clb_",
        "grid_clb_1__2_":"logical_tile_clb_mode_clb_",
        "grid_clb_2__1_":"logical_tile_clb_mode_clb_",
        "grid_clb_2__2_":"logical_tile_clb_mode_clb_",
        "sb_0__0_":"sb_0__0_",
        "sb_0__1_":"sb_0__1_",
        "sb_0__2_":"sb_0__2_",
        "sb_1__0_":"sb_1__0_",
        "sb_1__1_":"sb_1__1_",
        "sb_1__2_":"sb_1__2_",
        "sb_2__0_":"sb_2__0_",
        "sb_2__1_":"sb_2__1_",
        "sb_2__2_":"sb_2__2_",
        "cbx_1__0_":"cbx_1__0_",
        "cbx_2__0_":"cbx_1__0_",
        "cbx_1__1_":"cbx_1__1_",
        "cbx_2__1_":"cbx_1__1_",
        "cbx_1__2_":"cbx_1__2_",
        "cbx_2__2_":"cbx_1__2_",
        "cby_0__1_":"cby_0__1_",
        "cby_0__2_":"cby_0__1_",
        "cby_1__1_":"cby_1__1_",
        "cby_1__2_":"cby_1__1_",
        "cby_2__1_":"cby_2__1_",
        "cby_2__2_":"cby_2__1_",
    }

    ## iterate through each module at the top level
    for moduleName, module in modules.items():
        # print(module.type)

        if moduleName in module_mappings.keys():

            # ioCsvFile
            with open(f"{baseDir}/debug/bitstream_validator/mux_mappings/{module_mappings[moduleName]}.io","r+") as ioCsvFile:
                reader = csv.reader(ioCsvFile)
                # next(reader)
                for io in reader:
                    if int(io[1]) == 1:
                        newIO = IO(io[0], moduleName, io[2])
                        modules[moduleName].addIO(newIO)
                    else:
                        for i in range(int(io[1])):
                            newIO = IO(io[0] + f"[{i}]", moduleName, io[2])
                            modules[moduleName].addIO(newIO)
                    
            # muxCsvFile
            with open(f"{baseDir}/debug/bitstream_validator/mux_mappings/{module_mappings[moduleName]}.mux","r+") as muxCsvFile:
                reader = csv.reader(muxCsvFile)
                # next(reader)
                newNodes = []
                for muxLine in reader:

                    fixedMuxLine = []
                    for entry in muxLine: 
                        if x := re.match(r"(.+)\[(\d+):(\d+)\]",entry):
                            fixedMuxLine.append(x.group(1) + f"[{x.group(2)}]")
                            fixedMuxLine.append(x.group(1) + f"[{x.group(3)}]")
                        else:
                            fixedMuxLine.append(entry)

                    if "wire" in fixedMuxLine[1]:
                        modules[moduleName].mapIO(fixedMuxLine[2],fixedMuxLine[-1])

                    else:
                        for node in modules[moduleName].nodes:
                            
                            muxMemName = "mem" + fixedMuxLine[0][3:]

                            if node.name == muxMemName:
                                
                                newNode = None

                                if "size2" in fixedMuxLine[1]:
                                    newNode:MuxTreeSize2Node = MuxTreeSize2Node(node.name,fixedMuxLine[1],node.path,node.values)
                                elif "size3" in fixedMuxLine[1]:
                                    newNode:MuxTreeSize3Node = MuxTreeSize3Node(node.name,fixedMuxLine[1],node.path,node.values)
                                elif "size4" in fixedMuxLine[1]:
                                    newNode:MuxTreeSize4Node = MuxTreeSize4Node(node.name,fixedMuxLine[1],node.path,node.values)
                                elif "size5" in fixedMuxLine[1]:
                                    newNode:MuxTreeSize5Node = MuxTreeSize5Node(node.name,fixedMuxLine[1],node.path,node.values)
                                elif "size8" in fixedMuxLine[1]:
                                    newNode:MuxTreeSize8Node = MuxTreeSize8Node(node.name,fixedMuxLine[1],node.path,node.values)
                                elif "size9" in fixedMuxLine[1]:
                                    newNode:MuxTreeSize9Node = MuxTreeSize9Node(node.name,fixedMuxLine[1],node.path,node.values)
                                elif "size11" in fixedMuxLine[1]:
                                    newNode:MuxTreeSize11Node = MuxTreeSize11Node(node.name,fixedMuxLine[1],node.path,node.values)
                                elif "size12" in fixedMuxLine[1]:
                                    newNode:MuxTreeSize12Node = MuxTreeSize12Node(node.name,fixedMuxLine[1],node.path,node.values)
                                elif "size14" in fixedMuxLine[1]:
                                    newNode:MuxTreeSize14Node = MuxTreeSize14Node(node.name,fixedMuxLine[1],node.path,node.values)


                                newNodes.append(newNode)

                                muxChoice = newNode.getInputChoice()

                                if muxChoice != None:
                                    modules[moduleName].mapIO(fixedMuxLine[2+muxChoice],fixedMuxLine[-1],newNode)
                                else:
                                    if ("".join(map(str,node.values)) != len(newNode.values) * "0"):
                                        print("Routing node was not defaulted but still returned CONST1")
                                        print(f"\tValues: {node.values}")


                modules[moduleName].nodes = newNodes

        
        # for io in modules[moduleName].io.values():
        #     if io.nextIO != None:
        #         print(io)

    return modules

## This method parses the verilog module files for each top level module
## It then writes out all of the inputs and outputs for that top level module
## It also extracts information about the muxes that exist in that module and what they're connected to
def parseModules():

    all_files = [   "sb_0__2_",
                    "sb_0__1_",
                    "sb_1__0_",
                    "sb_1__1_",
                    "sb_1__2_",
                    "sb_2__1_",
                    "sb_2__0_",
                    "sb_2__2_",
                    "cbx_1__1_",
                    "cbx_1__0_",
                    "cby_1__1_",
                    "cby_0__1_",
                    "cbx_1__2_",
                    "cby_2__1_",
                    "sb_0__0_",
                    "logical_tile_clb_mode_clb_",
                    "grid_io_bottom",
                    "grid_io_top",
                    "grid_io_right",
                    "grid_io_left"
            ]
    ## for each module in fpga_top, we want to identify all of its io
    for moduleName in all_files:

        # open the verilog file corresponding to the current module and read its lines
        verilog_fh = None
        if "clb" in moduleName or "grid_io" in moduleName:
            verilog_fh = open(f"{resultsPath}/SRC/lb/{moduleName}.v","r+")
        else:
            verilog_fh = open(f"{resultsPath}/SRC/routing/{moduleName}.v","r+")
        verilogFileLines = verilog_fh.readlines()
        verilog_fh.close()

        # create an io file for the current module
        io_fh = open(f"{baseDir}/debug/bitstream_validator/mux_mappings/{moduleName}.io","w+")

        # go through each line of the verilog file and identify the input and outputs of the current module
        for line in verilogFileLines:
            parseLine = ("prog_clk" not in line) and ("ccff_head" not in line) and ("ccff_tail" not in line) and ("set" not in line) and ("reset" not in line) and ("clk" not in line)
            if parseLine:
                if x := re.match(r"(input) \[\d:(\d+)\] (.+);",line):
                    io_fh.write(f"{x.group(3)},{int(x.group(2)) + 1},{x.group(1)}\n")
                elif x := re.match(r"(output) \[\d:(\d+)\] (.+);",line):
                    io_fh.write(f"{x.group(3)},{int(x.group(2)) + 1},{x.group(1)}\n")
        io_fh.close()

    ## For Switch Box and CB Modules
    routing_files = [   "sb_0__2_",
                        "sb_0__1_",
                        "sb_1__0_",
                        "sb_1__1_",
                        "sb_1__2_",
                        "sb_2__1_",
                        "sb_2__0_",
                        "sb_2__2_",
                        "cbx_1__1_",
                        "cbx_1__0_",
                        "cby_1__1_",
                        "cby_0__1_",
                        "cbx_1__2_",
                        "cby_2__1_",
                        "sb_0__0_",
                        "logical_tile_clb_mode_clb_",
                        "grid_io_bottom",
                        "grid_io_top",
                        "grid_io_right",
                        "grid_io_left"
            ]
    
    # for each module in fpga_top, we want to identify the routing muxes
    for moduleName in routing_files:

        # open the verilog file corresponding to the current module and read its lines
        verilog_fh = None
        if "clb" in moduleName or "grid_io" in moduleName:
            verilog_fh = open(f"{resultsPath}/SRC/lb/{moduleName}.v","r+")
        else:
            verilog_fh = open(f"{resultsPath}/SRC/routing/{moduleName}.v","r+")
        verilogFileLines = verilog_fh.readlines()
        verilog_fh.close()

        # create a mux file for the current module
        mux_fh = open(f"{baseDir}/debug/bitstream_validator/mux_mappings/{moduleName}.mux","w+")

        # use a state variable to keep track of what has been processed so far for a given mux
        state = 0
        muxConfig = []

        for line in verilogFileLines:
            
            # if the line has "chan" in it, it might be a direct wire assignmnet
            if "chan" in line:
                if x := re.match(r"\tassign (.*) = (.*);", line):

                    # chan usually corresponds to multi-bit wires
                    # if the latter group has "chan", then remove the last 3 chars (why?)
                    # - probably did this because I didn't want the bit index from that wire?    
                    if "chan" not in x.group(2):
                        mux_fh.write(f"wire,wire,{x.group(2)[:-3]},None,{x.group(1)}\n") 
                    else:
                        mux_fh.write(f"wire,wire,{x.group(2)},None,{x.group(1)}\n") 
            
            # if in state 0, check for the beginning of a new mux
            if state == 0:

                # store the mux name and type if it is a mux
                if x := re.match(r"\t(mux_.*) (mux_.*) \(", line):
                    muxConfig.append(x.group(2))
                    muxConfig.append(x.group(1))
                    state = 1
                
                # else, check if its an io pad
                elif x := re.match(r"\s+logical_tile_io_mode_io_\s+(logical_tile_io_mode_io__\d+)", line):
                    muxConfig.append(x.group(1))
                    muxConfig.append(x.group(1))
                    state = 1


            # if in state 1, check for a mux input
            elif state == 1:

                if x := re.match(r"\t\t.in\({(.*)}", line):
                    muxInputs = x.group(1).split(",")
                    for muxInput in muxInputs:
                        if y := re.match(r"\s*(.+)\[(\d+):(\d+)\]",muxInput):
                            size = int(y.group(3))
                            for i in range(size):
                                muxConfig.append(f"{y.group(1)}[{i}]")
                        else:
                            muxConfig.append(muxInput.strip())
                    state = 2
                
                ## else, check for gpio data
                ## this would be the inout port
                elif x := re.match(r"\s+.gfpga_pad_GPIO_PAD\((.*)\),", line):
                    muxConfig.append(x.group(1))
                    state = 2

            # if in state 2, check for a mux output and reset the state
            elif state == 2:

                if x := re.match(r"\t\t.out\((.*)\)\);", line):
                    muxConfig.append(x.group(1))

                    # write the mux information out to the file once all the mux info has been parsed
                    mux_fh.write(",".join(muxConfig) + "\n")

                    muxConfig = []
                    state = 0
                
                elif x := re.match(r"\s+.io_outpad\((.*)\),", line):
                    muxConfig.append(x.group(1))
                    state = 3

            elif state == 3:
                if x := re.match(r"\s+.io_inpad\((.*)\),", line):
                    muxConfig.append(x.group(1))
                    mux_fh.write(",".join(muxConfig) + "\n")

                    muxConfig = []
                    state = 0


        mux_fh.close()