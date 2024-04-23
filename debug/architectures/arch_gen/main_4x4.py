# import sys
# sys.path.append('/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/scripts')

from architecture_generator.copy_bitstreams import *
from architecture_generator.make_designs import *
from architecture_generator.make_task_config import *
from architecture_generator.config_chain_extraction import *
from architecture_generator.bit_labeller import *
from architecture_generator.window_maker import *

from architecture_generator.windows_6x6 import *
from architecture_generator.windows_4x4 import *

import shutil
import os
import pathlib
import glob

# from openfpga_flow.scripts.run_fpga_task.py
# from run_fpga_task import main

def gen_designs(VERTICAL_CLB_COUNT, NUM_DESIGNS=20000):

    # Use all LUTs, but leave one CLB free
    NUM_LUTS = VERTICAL_CLB_COUNT*VERTICAL_CLB_COUNT*4 - 4
    SIZE= f"{VERTICAL_CLB_COUNT}x{VERTICAL_CLB_COUNT}"

    results_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)

    design_dir = f"{results_dir}/designs"
    info_dir = f"{results_dir}/_info"
    bitstreams_dir = f"{results_dir}/bitstreams"

    pathlib.Path(design_dir).mkdir(parents=True, exist_ok=False)
    pathlib.Path(info_dir).mkdir(parents=True, exist_ok=False)
    pathlib.Path(bitstreams_dir).mkdir(parents=True, exist_ok=False)

    make_tiered_il_designs(design_dir, NUM_DESIGNS, NUM_LUTS=NUM_LUTS)
    
    write_task_config(info_dir, design_dir, NUM_DESIGNS, SIZE)

    shutil.copy(f"{info_dir}/task.conf", f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/config/task.conf")

    
    # run_task_config()

    # python3 openfpga_flow/scripts/run_fpga_task.py basic_tests/0_debug_task/fpga_4x4_clb

def analyze_designs(VERTICAL_CLB_COUNT):
    # openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/latest/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/SRC/fpga_top.v

    SIZE = f"{VERTICAL_CLB_COUNT}x{VERTICAL_CLB_COUNT}"
    results_dir = f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/latest/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
    output_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb"
    info_output_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb/_info"
    bitstreams_output_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb/bitstreams"

    top_level = f"{results_dir}/SRC/fpga_top.v"
    moduleConfigOrder = config_chain_extraction(top_level)

    xml_bitstream = f"{results_dir}/fabric_independent_bitstream.xml"
    module_info, bit_mapping = bitstream_label(moduleConfigOrder, xml_bitstream, info_output_dir)

    module_layout_grid = get_module_layout_grid(module_info, VERTICAL_CLB_COUNT)
    # device_visualization(module_layout_grid, module_info, moduleConfigOrder)

    # Copy bitstreams
    # NUM_DESIGNS = 20000
    # for i in range(NUM_DESIGNS):
    #     idx = f"{i}".zfill(5)
    #     bitstream_file = f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/latest/k4_N4_tileable_40nm_new/bench{i}_fpga_design/MIN_ROUTE_CHAN_WIDTH/fabric_bitstream.bit"
    #     shutil.copy(f"{bitstream_file}",f"{bitstreams_output_dir}/{idx}.bit")



    # Make windowed bitstream files

    # First let's make the directories and store a reference to them
    # window_dirs = []
    # for i in range(len(windows_4x4)):

    #     # make window directory
    #     window_dir = f"{output_dir}/window_{i}"
    #     window_dirs.append(window_dir)
    #     if os.path.exists(window_dir):
    #         shutil.rmtree(window_dir)
    #     pathlib.Path(window_dir).mkdir(parents=True, exist_ok=False)
    
    # # Now lets iterate through each bitstream and extract the windowed bits
    # bitstream_paths = glob.glob(f"{bitstreams_output_dir}/*")
    # for index in range(len(bitstream_paths)):
    #     string_index = f"{index}".zfill(5)
    #     bitstream_path = bitstream_paths[index]
    #     bitstream_fh = open(bitstream_path, "r+")
    #     bitstream_lines = bitstream_fh.readlines()[5:]
    #     bitstream_fh.close()
        
    #     # Lets open a window file for this bitstream for each of the 4 window types
    #     fh_list = []
    #     for i in range(len(window_dirs)):
    #         window_dir = window_dirs[i]
    #         fh = open(f"{window_dir}/{string_index}.window{i}.bit","w+")
    #         fh_list.append(fh)

    #     # Now lets go through each bit of the bitstream and determine which windows it should be copied into
    #     for bit_index in range(len(bitstream_lines)):

    #         # Loop through each window
    #         for window_index in range(len(windows_4x4)):
    #             window = windows_4x4[window_index]

    #             # If the bit belongs to a module that is part of the current window, then write it to the bitstream's window file
    #             if bit_mapping[bit_index]["module name"] in window:
    #                 bit = bitstream_lines[bit_index]
    #                 fh_list[window_index].write(bit)
        
    #     # Now close all of the window files for this bitstream
    #     for fh in fh_list:
    #         fh.close()
    
    # Finally lets make a reference for each of the windows so we know the bit mappings
    bitstream_path = f"{bitstreams_output_dir}/00000.bit"
    bitstream_fh = open(bitstream_path, "r+")
    bitstream_lines = bitstream_fh.readlines()[5:]
    bitstream_fh.close()
    
    # Lets open a window file for this bitstream for each of the 4 window types
    for window_index in range(len(windows_4x4)):
        window_label_path= info_output_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb/_info"
        fh = open(f"{window_label_path}/window_{window_index}_labels.csv","w+")
        fh.write("module_name,path,name,bit\n")

        # Now lets go through each bit of the bitstream and determine which windows it should be copied into
        for bit_index in range(len(bitstream_lines)):

            window = windows_4x4[window_index]

            # If the bit belongs to a module that is part of the current window, then write it to the bitstream's window file
            if bit_mapping[bit_index]["module name"] in window:
                bit = bitstream_lines[bit_index].strip()

                bit_string = ""
                bit_string += f"{bit_mapping[bit_index]['module name']}," 
                bit_string += f"{bit_mapping[bit_index]['node path']}," 
                bit_string += f"{bit_mapping[bit_index]['node name']}," 
                bit_string += f"{bit}\n" 

                fh.write(bit_string)
        
        fh.close()



    # results_dir = f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/latest/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
    # copy_bitstreams(results_dir, bitstreams_output_dir, 20000)

if __name__ == "__main__":
    gen_designs(4,20000)
    # analyze_designs(4)