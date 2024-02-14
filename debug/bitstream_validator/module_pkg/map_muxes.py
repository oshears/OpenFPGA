from . import *
# from module_classes import *
# import module_pkg.module_classes.Module
from .module_classes import *

### get muxes and io, and map them to the modules
def mapMuxes(modules:dict[str,Module]):

    module_mappings = {
        "grid_io_top_1__3_":"grid_io_top",
        "grid_io_top_2__3_":"grid_io_top",
        "grid_io_right_3__2_":"grid_io_right",
        "grid_io_right_3__1_":"grid_io_right",
        "grid_io_bottom_2__0_":"grid_io_bottom",
        "grid_io_bottom_1__0_":"grid_io_bottom",
        "grid_io_left_0__1_":"grid_io_left",
        "grid_io_left_0__2_":"grid_io_left",
        "grid_clb_1__1_":"grid_clb",
        "grid_clb_1__2_":"grid_clb",
        "grid_clb_2__1_":"grid_clb",
        "grid_clb_2__2_":"grid_clb",
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

        # if the current module is in the list of module names to performing mapping on
        if moduleName in module_mappings.keys():

            # open the module's io csv file and create a new IO instance to place in that module
            # TODO: maybe it'd be a good idea to add these IO to the mux classes (if I ever get around to making them)
            with open(f"{baseDir}/debug/bitstream_validator/mux_mappings/{module_mappings[moduleName]}.io","r+") as ioCsvFile:
                reader = csv.reader(ioCsvFile)
                for io in reader:
                    # if IO has only one bit, add it and indicate its direction
                    if int(io[1]) == 1:
                        newIO = IO(io[0], moduleName, io[2])
                        modules[moduleName].addIO(newIO)
                    else:
                        # unpacked any IO that are have more than one bit
                        for i in range(int(io[1])):
                            newIO = IO(io[0] + f"[{i}]", moduleName, io[2])
                            modules[moduleName].addIO(newIO)
                    
            # now open the multiplex info file for the current module
            with open(f"{baseDir}/debug/bitstream_validator/mux_mappings/{module_mappings[moduleName]}.mux","r+") as muxCsvFile:
                reader = csv.reader(muxCsvFile)

                # we will make a new Node for each multiplexer to replace the generic original nodes
                newNodes = []

                # for each line in the muxCsvFile for the current module
                for muxLine in reader:
                    
                    # correct the formatting of the inputs to the mux if any of them have multiple bits (e.g., someWire[0:19])
                    fixedMuxLine = []
                    for entry in muxLine: 
                        if x := re.match(r"(.+)\[(\d+):(\d+)\]",entry):
                            fixedMuxLine.append(x.group(1) + f"[{x.group(2)}]")
                            fixedMuxLine.append(x.group(1) + f"[{x.group(3)}]")
                        else:
                            fixedMuxLine.append(entry)

                    # if the current entry is just a wire, then directly map the IOs from input to output
                    if "wire" in fixedMuxLine[1]:
                        modules[moduleName].mapIO(fixedMuxLine[2], fixedMuxLine[-1], directConnection=True)

                    # if the current entry is a GPIO pad
                    elif "logical_tile_io_mode_io" in fixedMuxLine[1]:
                        # print(moduleName)
                        for node in modules[moduleName].nodes:
                            # print(f"\t{node.path.split('/')[1]}")
                            nodeName = node.path.split("/")[1]
                            if nodeName == fixedMuxLine[0]:
                                newNode = GPIO_PAD(nodeName,fixedMuxLine[1],node.path,node.values[0])
                                newNodes.append(newNode)

                                gpioSetting = newNode.getSetting()

                                if gpioSetting == 'in_pad':
                                    modules[moduleName].mapIO(fixedMuxLine[2],fixedMuxLine[4],newNode)
                                else:
                                    modules[moduleName].mapIO(fixedMuxLine[3],fixedMuxLine[2],newNode)
                    
                    # else it is a regular multiplexer
                    else:
                        # we must search through all of the existing generic nodes in the current top level module
                        # for the node we have to replace
                        for node in modules[moduleName].nodes:
                            
                            muxMemName = "mem" + fixedMuxLine[0][3:]

                            # if we have found the node that needs to be replaced, we can start to replace it here 
                            if node.name == muxMemName:
                                
                                newNode = None

                                # determine what type of node to replace it with
                                # each of these nodes has a specific way of determining which input to send to the output
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

                                # get the index of the input the mux is configured to select/propagate
                                muxChoice = newNode.getInputChoice()

                                if muxChoice != None:
                                    # print(moduleName)
                                    # print(fixedMuxLine[2+muxChoice])
                                    # print(fixedMuxLine[-1])
                                    # print(newNode)

                                    # if the current module is a CLB, we have to do a translation in order to get the proper io name
                                    if "clb" in moduleName:
                                        clb_io_mappings = {
                                            "clb_I[0]":"top_width_0_height_0_subtile_0__pin_I_0_",
                                            "clb_I[1]":"right_width_0_height_0_subtile_0__pin_I_1_",
                                            "clb_I[2]":"bottom_width_0_height_0_subtile_0__pin_I_2_",
                                            "clb_I[3]":"left_width_0_height_0_subtile_0__pin_I_3_",
                                            "clb_I[4]":"top_width_0_height_0_subtile_0__pin_I_4_",
                                            "clb_I[5]":"right_width_0_height_0_subtile_0__pin_I_5_",
                                            "clb_I[6]":"bottom_width_0_height_0_subtile_0__pin_I_6_",
                                            "clb_I[7]":"left_width_0_height_0_subtile_0__pin_I_7_",
                                            "clb_I[8]":"top_width_0_height_0_subtile_0__pin_I_8_",
                                            "clb_I[9]":"right_width_0_height_0_subtile_0__pin_I_9_",
                                            "clb_O[0]":"bottom_width_0_height_0_subtile_0__pin_O_0_",
                                            "clb_O[1]":"left_width_0_height_0_subtile_0__pin_O_1_",
                                            "clb_O[2]":"top_width_0_height_0_subtile_0__pin_O_2_",
                                            "clb_O[3]":"right_width_0_height_0_subtile_0__pin_O_3_",
                                            "logical_tile_clb_mode_default__fle_0_fle_out":"logical_tile_clb_mode_default__fle_0_fle_out",
                                            "logical_tile_clb_mode_default__fle_1_fle_out":"logical_tile_clb_mode_default__fle_1_fle_out",
                                            "logical_tile_clb_mode_default__fle_2_fle_out":"logical_tile_clb_mode_default__fle_2_fle_out",
                                            "logical_tile_clb_mode_default__fle_3_fle_out":"logical_tile_clb_mode_default__fle_3_fle_out"
                                        }
                                        # clb_fle_mappings = {
                                        #     "logical_tile_clb_mode_default__fle_0_fle_out":"clb_0[0]",
                                        #     "logical_tile_clb_mode_default__fle_1_fle_out":"clb_0[1]",
                                        #     "logical_tile_clb_mode_default__fle_2_fle_out":"clb_0[2]",
                                        #     "logical_tile_clb_mode_default__fle_3_fle_out":"clb_0[3]",
                                        # }
                                        clb_fle_out_mappings = {
                                            "mux_tree_size14_0_out":"bottom_width_0_height_0_subtile_0__pin_O_0_",
                                            "mux_tree_size14_1_out":"bottom_width_0_height_0_subtile_0__pin_O_0_",
                                            "mux_tree_size14_2_out":"bottom_width_0_height_0_subtile_0__pin_O_0_",
                                            "mux_tree_size14_3_out":"bottom_width_0_height_0_subtile_0__pin_O_0_",
                                            "mux_tree_size14_4_out":"left_width_0_height_0_subtile_0__pin_O_1_",
                                            "mux_tree_size14_5_out":"left_width_0_height_0_subtile_0__pin_O_1_",
                                            "mux_tree_size14_6_out":"left_width_0_height_0_subtile_0__pin_O_1_",
                                            "mux_tree_size14_7_out":"left_width_0_height_0_subtile_0__pin_O_1_",
                                            "mux_tree_size14_8_out":"top_width_0_height_0_subtile_0__pin_O_2_",
                                            "mux_tree_size14_9_out":"top_width_0_height_0_subtile_0__pin_O_2_",
                                            "mux_tree_size14_10_out":"top_width_0_height_0_subtile_0__pin_O_2_",
                                            "mux_tree_size14_11_out":"top_width_0_height_0_subtile_0__pin_O_2_",
                                            "mux_tree_size14_12_out":"right_width_0_height_0_subtile_0__pin_O_3_",
                                            "mux_tree_size14_13_out":"right_width_0_height_0_subtile_0__pin_O_3_",
                                            "mux_tree_size14_14_out":"right_width_0_height_0_subtile_0__pin_O_3_",
                                            "mux_tree_size14_15_out":"right_width_0_height_0_subtile_0__pin_O_3_",
                                        }
                                        cross_fle_inputs = [
                                            "logical_tile_clb_mode_default__fle_0_fle_out",
                                            "logical_tile_clb_mode_default__fle_1_fle_out",
                                            "logical_tile_clb_mode_default__fle_2_fle_out",
                                            "logical_tile_clb_mode_default__fle_3_fle_out"
                                        ]

                                        # map the input that the mux is configured to select to...
                                        translatedInput = clb_io_mappings[fixedMuxLine[2+muxChoice]]
                                        # translatedOutput = clb_io_mappings[fixedMuxLine[-1]]
                                        translatedOutput = clb_fle_out_mappings[fixedMuxLine[-1]]
                                        if "logical_tile_clb_mode_default__fle_" in translatedInput:
                                            ## Temporary, map internal IO only
                                            modules[moduleName].mapInternalIO(translatedInput,translatedOutput, newNode)
                                            # newNode.setInput(modules[moduleName].io[translatedInput])
                                            # newNode.setOutput(modules[moduleName].io[translatedOutput])
                                        else:
                                            modules[moduleName].mapIO(translatedInput,translatedOutput, newNode)
                                    
                                    # all other non-CLB cases
                                    else:
                                        # map the input that the mux is configured to select to...
                                        modules[moduleName].mapIO(fixedMuxLine[2+muxChoice],fixedMuxLine[-1], newNode)
                                        
                                        # configured mux association
                                        newNode.setInput(modules[moduleName].io[fixedMuxLine[2+muxChoice]])
                                        newNode.setOutput(modules[moduleName].io[fixedMuxLine[-1]])
                                        modules[moduleName].io[fixedMuxLine[2+muxChoice]].mux = newNode
                                        modules[moduleName].io[fixedMuxLine[-1]].mux = newNode
                                        
                                else:
                                    if ("".join(map(str,node.values)) != len(newNode.values) * "0"):
                                        print("Routing node was not defaulted but still returned CONST1")
                                        print(f"\tValues: {node.values}")


                modules[moduleName].nodes = newNodes

    return modules

