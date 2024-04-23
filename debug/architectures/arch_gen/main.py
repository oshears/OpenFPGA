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

# from openfpga_flow.scripts.run_fpga_task.py
# from run_fpga_task import main

def gen_4x4_designs(NUM_DESIGNS=20000):

    NUM_LUTS = 4*4*4
    SIZE= "4x4"

    results_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)

    design_dir = f"{results_dir}/designs"
    info_dir = f"{results_dir}/_info"

    pathlib.Path(design_dir).mkdir(parents=True, exist_ok=False)
    pathlib.Path(info_dir).mkdir(parents=True, exist_ok=False)

    make_tiered_il_designs(design_dir, NUM_DESIGNS, NUM_LUTS=NUM_LUTS)
    
    write_task_config(info_dir, design_dir, NUM_DESIGNS, SIZE)

    shutil.copy(f"{info_dir}/task.conf", f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/config/task.conf")

    
    # run_task_config()

    # python3 openfpga_flow/scripts/run_fpga_task.py basic_tests/0_debug_task/fpga_4x4_clb

def gen_6x6_designs(NUM_DESIGNS=1):

    NUM_LUTS = 6*6*4 - 4
    SIZE= "6x6"

    results_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb"
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)

    design_dir = f"{results_dir}/designs"
    info_dir = f"{results_dir}/_info"

    pathlib.Path(design_dir).mkdir(parents=True, exist_ok=False)
    pathlib.Path(info_dir).mkdir(parents=True, exist_ok=False)

    open_fpga_dir = f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/config/"
    if not os.path.exists(open_fpga_dir):
        pathlib.Path(open_fpga_dir).mkdir(parents=True, exist_ok=False)

    make_tiered_il_designs(design_dir, NUM_DESIGNS, NUM_LUTS=NUM_LUTS)
    
    write_task_config(info_dir, design_dir, NUM_DESIGNS, SIZE)

    shutil.copy(f"{info_dir}/task.conf", f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/config/task.conf")

def analyze_4x4_designs():
    # design_source_dir = "/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
    # design_source_dir = "openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
    design_source_dir = "openfpga_flow/tasks/basic_tests/0_debug_task/design_analysis/latest/k4_N4_tileable_40nm_new/fpga_design/MIN_ROUTE_CHAN_WIDTH"
    output_dir = "debug/architectures/arch_gen/results/fpga_4x4_clb/_info/"

    top_level = f"{design_source_dir}/SRC/fpga_top.v"
    # results = config_chain_extraction(top_level)
    moduleConfigOrder = config_chain_extraction(top_level)

    xml_bitstream = f"{design_source_dir}/fabric_independent_bitstream.xml"
    module_info = bitstream_label(moduleConfigOrder, xml_bitstream)

    module_layout_grid = get_module_layout_grid(module_info, 4)
    device_visualization(module_layout_grid, module_info, moduleConfigOrder)

    # for module in module_info:
    #     print(f"{module} : {len(module_info[module])}")
    for window_modules in windows_4x4:
        make_windows(module_info, window_modules)

def analyze_designs(VERTICAL_CLB_COUNT=6):
    SIZE = f"{VERTICAL_CLB_COUNT}x{VERTICAL_CLB_COUNT}"
    design_source_dir = f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/latest/k4_N4_tileable_40nm_new/fpga_design/MIN_ROUTE_CHAN_WIDTH"
    output_dir = f"debug/architectures/arch_gen/results/fpga_{SIZE}_clb/_info/"

    top_level = f"{design_source_dir}/SRC/fpga_top.v"
    moduleConfigOrder = config_chain_extraction(top_level)

    xml_bitstream = f"{design_source_dir}/fabric_independent_bitstream.xml"
    module_info = bitstream_label(moduleConfigOrder, xml_bitstream, output_dir)

    module_layout_grid = get_module_layout_grid(module_info, VERTICAL_CLB_COUNT)
    device_visualization(module_layout_grid, module_info, moduleConfigOrder)

    for window_modules in windows_6x6:
        make_windows(module_info, window_modules)

if __name__ == "__main__":
    # generate_il_designs()
    # write_task_config()
    # run_task_config(NUM_DESIGNS=5000)

    # 1. Doubled Device Size, Simialar Connections
    # gen_4x4_designs()
    # analyze_4x4_designs()

    gen_6x6_designs()
    # analyze_designs(VERTICAL_CLB_COUNT=6)

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
    