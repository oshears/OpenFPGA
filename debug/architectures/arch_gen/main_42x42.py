# import sys
# sys.path.append('/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/scripts')

from architecture_generator.copy_bitstreams import *
from architecture_generator.make_designs import *
from architecture_generator.make_task_config import *
from architecture_generator.config_chain_extraction import *
from architecture_generator.bit_labeller import *
from architecture_generator.window_maker import *
from architecture_generator.make_readme import *

from architecture_generator.generate_windows import generate_windows

import shutil
import os
import pathlib
import glob

import pickle

# from openfpga_flow.scripts.run_fpga_task.py
# from run_fpga_task import main

# def gen_4x4_designs(NUM_DESIGNS=20000,route_chan_width=40):

#     NUM_LUTS = 4*4*4
#     SIZE= "4x4"

#     results_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb"
#     if os.path.exists(results_dir):
#         shutil.rmtree(results_dir)

#     design_dir = f"{results_dir}/designs"
#     info_dir = f"{results_dir}/_info"

#     pathlib.Path(design_dir).mkdir(parents=True, exist_ok=False)
#     pathlib.Path(info_dir).mkdir(parents=True, exist_ok=False)

#     make_tiered_il_designs(design_dir, NUM_DESIGNS, NUM_LUTS=NUM_LUTS)
    
#     write_task_config(info_dir, design_dir, NUM_DESIGNS, SIZE, route_chan_width=route_chan_width)

#     shutil.copy(f"{info_dir}/task.conf", f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/config/task.conf")

    
#     # run_task_config()

#     # python3 openfpga_flow/scripts/run_fpga_task.py basic_tests/0_debug_task/fpga_4x4_clb

def gen_42x42_designs(NUM_DESIGNS=1, route_chan_width=42):

    NUM_LUTS = 42*42*4 - 4
    SIZE= "42x42"

    dir_name = "openfpga__arch_42x42__tiered_luts__20240516"

    results_dir = f"debug/architectures/arch_gen/results/{dir_name}"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)

    design_dir = f"{results_dir}/designs"
    info_dir = f"{results_dir}/_info"

    pathlib.Path(design_dir).mkdir(parents=True, exist_ok=False)
    pathlib.Path(info_dir).mkdir(parents=True, exist_ok=False)

    open_fpga_dir = f"openfpga_flow/tasks/basic_tests/0_debug_task/{dir_name}/config/"
    if not os.path.exists(open_fpga_dir):
        pathlib.Path(open_fpga_dir).mkdir(parents=True, exist_ok=False)

    make_tiered_il_designs(design_dir, 42, NUM_DESIGNS, NUM_LUTS=NUM_LUTS)
    
    write_task_config(info_dir, design_dir, NUM_DESIGNS, SIZE, route_chan_width=route_chan_width)

    shutil.copy(f"{info_dir}/task.conf", f"openfpga_flow/tasks/basic_tests/0_debug_task/{dir_name}/config/task.conf")

# def analyze_4x4_designs():
#     # design_source_dir = "/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
#     # design_source_dir = "openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
#     design_source_dir = "openfpga_flow/tasks/basic_tests/0_debug_task/design_analysis/latest/k4_N4_tileable_40nm_new/fpga_design/MIN_ROUTE_CHAN_WIDTH"
#     output_dir = "debug/architectures/arch_gen/results/fpga_4x4_clb/_info/"

#     top_level = f"{design_source_dir}/SRC/fpga_top.v"
#     # results = config_chain_extraction(top_level)
#     moduleConfigOrder = config_chain_extraction(top_level)

#     xml_bitstream = f"{design_source_dir}/fabric_independent_bitstream.xml"
#     module_info = bitstream_label(moduleConfigOrder, xml_bitstream)

#     module_layout_grid = get_module_layout_grid(module_info, 4)
#     device_visualization(module_layout_grid, module_info, moduleConfigOrder)

#     # for module in module_info:
#     #     print(f"{module} : {len(module_info[module])}")
#     for window_modules in windows_4x4:
#         make_windows(module_info, window_modules)

# def analyze_designs(VERTICAL_CLB_COUNT=6):
#     SIZE = f"{VERTICAL_CLB_COUNT}x{VERTICAL_CLB_COUNT}"
#     design_source_dir = f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/latest/k4_N4_tileable_40nm_new/fpga_design/MIN_ROUTE_CHAN_WIDTH"
#     output_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb/_info/"

#     top_level = f"{design_source_dir}/SRC/fpga_top.v"
#     moduleConfigOrder = config_chain_extraction(top_level)

#     xml_bitstream = f"{design_source_dir}/fabric_independent_bitstream.xml"
#     module_info = bitstream_label(moduleConfigOrder, xml_bitstream, output_dir)

#     module_layout_grid = get_module_layout_grid(module_info, VERTICAL_CLB_COUNT)
#     device_visualization(module_layout_grid, module_info, moduleConfigOrder)

#     for window_modules in windows:
#         make_windows(module_info, window_modules)

def validate_windows(grid, windows):

    config_order = []
    
    for module_name in windows[0]:
        window_order = 0
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if module_name == grid[x][y]:
                    config_order.append(window_order)
                    print(window_order)

                if grid[x][y] in windows[0]:
                    window_order += 1
    
    for window in windows[1:]:
        print("Next Window:")
        for module_name_idx in range(len(window)):
            window_order = 0
            for x in range(len(grid)):
                for y in range(len(grid[x])):

                    if window[module_name_idx] == grid[x][y]:
                        if window_order != config_order[module_name_idx]:
                            raise Exception("Windows are not aligned! Module config positions are mismatched!")
                        else:
                            print(window_order)

                    if grid[x][y] in window:
                        window_order += 1

def analyze_designs(VERTICAL_CLB_COUNT, dataset_name=None, overwrite=False, load=True):
    # openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/latest/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/SRC/fpga_top.v

    dir_name = "openfpga__arch_42x42__tiered_luts__20240516"

    NUM_LUTS = VERTICAL_CLB_COUNT*VERTICAL_CLB_COUNT*4 - 4
    SIZE = f"{VERTICAL_CLB_COUNT}x{VERTICAL_CLB_COUNT}"
    results_dir = f"openfpga_flow/tasks/basic_tests/0_debug_task/{dir_name}/latest/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
    output_dir = f"debug/architectures/arch_gen/results/{dir_name}"
    # output_dir = f"debug/architectures/arch_gen/results/openfpga__arch_6x6__lut_140__tiered_luts__20240429"
    info_output_dir = f"{output_dir}/_info"
    bitstreams_output_dir = f"{output_dir}/bitstreams"

    if not os.path.exists(bitstreams_output_dir):
        pathlib.Path(bitstreams_output_dir).mkdir(parents=True, exist_ok=False)


    # TODO: might want to make these data values into pickle files 
    top_level = f"{results_dir}/SRC/fpga_top.v"
    # moduleConfigOrder = config_chain_extraction(top_level)
    moduleConfigOrder = None
    if load:
        with open(f'{info_output_dir}/module_config_order.pkl',"rb") as file:
            moduleConfigOrder = pickle.load(file)

    if overwrite:
        with open(f'{info_output_dir}/module_config_order.pkl',"wb") as file:
            pickle.dump(moduleConfigOrder, file)

    xml_bitstream = f"{results_dir}/fabric_independent_bitstream.xml"
    # module_info, bit_mapping = bitstream_label(moduleConfigOrder, xml_bitstream, info_output_dir)
    module_info = None
    bit_mapping = None

    if load:
        with open(f'{info_output_dir}/module_info.pkl',"rb") as file:
            module_info = pickle.load(file)
        
        with open(f'{info_output_dir}/bit_mapping.pkl',"rb") as file:
            bit_mapping = pickle.load(file)

    if overwrite:
        with open(f'{info_output_dir}/module_info.pkl',"wb") as file:
            pickle.dump(module_info, file)

        with open(f'{info_output_dir}/bit_mapping.pkl',"wb") as file:
            pickle.dump(bit_mapping, file)

    # return

    module_layout_grid = get_module_layout_grid(module_info, VERTICAL_CLB_COUNT)
    # device_visualization(module_layout_grid, module_info, moduleConfigOrder)

    # Ensure that the grid positioning of all the windows are in alignment
    windows = generate_windows(VERTICAL_CLB_COUNT)
    # validate_windows(module_layout_grid, windows_42x42)

    # Copy bitstreams
    # NUM_DESIGNS = 20000
    NUM_DESIGNS = 14
    for i in range(NUM_DESIGNS):
        idx = f"{i}".zfill(5)
        bitstream_file = f"openfpga_flow/tasks/basic_tests/0_debug_task/{dir_name}/latest/k4_N4_tileable_40nm_new/bench{i}_fpga_design/MIN_ROUTE_CHAN_WIDTH/fabric_bitstream.bit"
        shutil.copy(f"{bitstream_file}",f"{bitstreams_output_dir}/{idx}.bit")

    # Make windowed bitstream files

    # First let's make the directories and store a reference to them
    window_dirs = []
    for i in range(len(windows)):

        # make window directory
        window_dir = f"{output_dir}/partition_{i}"
        window_dirs.append(window_dir)
        if os.path.exists(window_dir):
            shutil.rmtree(window_dir)
        pathlib.Path(window_dir).mkdir(parents=True, exist_ok=False)
    
    # Now lets iterate through each bitstream and extract the windowed bits
    bitstream_paths = glob.glob(f"{bitstreams_output_dir}/*")
    for index in range(len(bitstream_paths)):
        bitstream_progress = 100 * index // len(bitstream_paths)
        if index % (len(bitstream_paths) // 10) == 0:
            print(f"bitstreams processed: {bitstream_progress}%")
        
        string_index = f"{index}".zfill(5)
        bitstream_path = bitstream_paths[index]
        bitstream_fh = open(bitstream_path, "r+")
        bitstream_lines = bitstream_fh.readlines()[5:]
        bitstream_fh.close()
        
        # Lets open a window file for this bitstream for each of the 4 window types
        fh_list = []
        for i in range(len(window_dirs)):
            window_dir = window_dirs[i]
            fh = open(f"{window_dir}/{string_index}.partition{i}.bit","w+")
            fh_list.append(fh)

        # Now lets go through each bit of the bitstream and determine which windows it should be copied into
        for bit_index in range(len(bitstream_lines)):

            # Loop through each window
            for window_index in range(len(windows)):
                window = windows[window_index]

                # If the bit belongs to a module that is part of the current window, then write it to the bitstream's window file
                if bit_mapping[bit_index]["module name"] in window:
                    bit = bitstream_lines[bit_index]
                    fh_list[window_index].write(bit)
        
        # Now close all of the window files for this bitstream
        for fh in fh_list:
            fh.close()
    
    # Finally lets make a reference for each of the windows so we know the bit mappings
    bitstream_path = f"{bitstreams_output_dir}/00000.bit"
    bitstream_fh = open(bitstream_path, "r+")
    bitstream_lines = bitstream_fh.readlines()[5:]
    bitstream_fh.close()
    
    # Lets open a window file for this bitstream for each of the 4 window types
    for window_index in range(len(windows)):
        window_progress = 100 * window_index / len(windows)
        print(f"window mappings created: {window_progress}%")

        window_label_path= info_output_dir = f"debug/architectures/arch_gen/results/{dir_name}/_info"
        fh = open(f"{window_label_path}/window_{window_index}_labels.csv","w+")
        fh.write("module_name,path,name,bit\n")

        # Now lets go through each bit of the bitstream and determine which windows it should be copied into
        for bit_index in range(len(bitstream_lines)):

            window = windows[window_index]

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
    
    # Lastly, make the readme for this data set
    make_readme(output_dir, VERTICAL_CLB_COUNT, NUM_LUTS, module_layout_grid, module_info, moduleConfigOrder, windows)


if __name__ == "__main__":
    # generate_il_designs()
    # write_task_config()
    # run_task_config(NUM_DESIGNS=5000)

    # 1. Doubled Device Size, Simialar Connections
    # gen_4x4_designs()
    # analyze_4x4_designs()

    # gen_42x42_designs(14, route_chan_width=128)
    analyze_designs(VERTICAL_CLB_COUNT=42)

    # 2. Doubled Device Size, Tiered LUT Connections
    # gen_4x4_designs(tiered_luts=True)

    # python3 openfpga_flow/scripts/run_fpga_task.py openfpga_flow/tasks/basic_tests/0_debug_task/design_analysis --maxthreads 10
    # cmd = ""
    # cmd += "cd /home/oshears/Documents/openfpga/OpenFPGA/ && bash openfpga.sh"
    # cmd += "python3 openfpga_flow/scripts/run_fpga_task.py "
    # cmd += "openfpga_flow/tasks/basic_tests/0_debug_task/design_analysis "
    # cmd += "--maxthreads 10 "
    # cmd += "--debug "

    # NOTE: Do I need to run open_fpga.sh before launching this task?
    # os.system(cmd)
    # if result != 0:
    #     print("THE TEST FAILED!")


    # copy_bitstreams()
    