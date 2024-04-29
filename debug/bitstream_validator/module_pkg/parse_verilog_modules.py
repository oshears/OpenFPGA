from . import *
# from module_classes import *
# import module_pkg.module_classes.Module
from .module_classes import *

import glob
import os
import re

def parseModules(baseDir, resultsPath):
    '''
    This method parses the verilog module files for each top level module

    It then writes out all of the inputs and outputs for that top level module
    
    It also extracts information about the muxes that exist in that module and what they're connected to
    '''

    source_paths = []
    source_paths += glob.glob(f"{resultsPath}/SRC/routing/*.v")
    source_paths += glob.glob(f"{resultsPath}/SRC/lb/grid_io_*.v")
    source_paths += glob.glob(f"{resultsPath}/SRC/lb/grid_clb.v")

    ## for each module in fpga_top, we want to identify all of its io
    for source_path in source_paths:

        moduleName = os.path.basename(source_path)[:-2]

        # open the verilog file corresponding to the current module and read its lines
        verilog_fh = open(source_path,"r+")
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
                elif x := re.match(r"(inout) \[\d:(\d+)\] (.+);",line):
                    io_fh.write(f"{x.group(3)},{int(x.group(2)) + 1},{x.group(1)}\n")
        io_fh.close()

    source_paths = []
    source_paths += glob.glob(f"{resultsPath}/SRC/routing/*.v")
    source_paths += glob.glob(f"{resultsPath}/SRC/lb/grid_io_*.v")
    source_paths += glob.glob(f"{resultsPath}/SRC/lb/logical_tile_clb_mode_clb_.v")
    
    # for each module in fpga_top, we want to identify the routing muxes
    for source_path in source_paths:

        moduleName = os.path.basename(source_path)[:-2]

        # open the verilog file corresponding to the current module and read its lines
        verilog_fh = open(source_path,"r+")
        verilogFileLines = verilog_fh.readlines()
        verilog_fh.close()

        # create a mux file for the current module
        mux_fh = None
        if "clb" in moduleName:
            mux_fh = open(f"{baseDir}/debug/bitstream_validator/mux_mappings/grid_clb.mux","w+")
        else:
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
                            start = int(y.group(2))
                            end = int(y.group(3)) + 1
                            for i in range(start, end):
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