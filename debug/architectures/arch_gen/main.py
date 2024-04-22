# import sys
# sys.path.append('/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/scripts')

from architecture_generator.copy_bitstreams import *
from architecture_generator.gen_designs import *
from architecture_generator.task_config import *
from architecture_generator.config_chain_extraction import *
from architecture_generator.bit_labeller import *
from architecture_generator.window_maker import *

import os

# from openfpga_flow.scripts.run_fpga_task.py
# from run_fpga_task import main

def gen_4x4_designs(NUM_DESIGNS=5000):
    # generate_il_designs(5000, NUM_LUTS=64, outdir="fpga_4x4_clb")
    # write_task_config(5000,"4x4", device_arch="")


    NUM_LUTS = 64
    # generate_il_designs(NUM_DESIGNS, NUM_LUTS=NUM_LUTS, outdir="fpga_4x4_clb")
    write_task_config(NUM_DESIGNS, "4x4", outdir="fpga_4x4_clb/designs", bench_dir="debug/architectures/arch_gen/results/fpga_4x4_clb/_info")
    shutil.copy("debug/architectures/arch_gen/results/fpga_4x4_clb/_info/task.conf","openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/config/task.conf")

    
    # run_task_config()

    # python3 openfpga_flow/scripts/run_fpga_task.py basic_tests/0_debug_task/fpga_4x4_clb


def analyze_4x4_designs():
    # design_source_dir = "/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
    design_source_dir = "openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/run018/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"

    top_level = f"{design_source_dir}/SRC/fpga_top.v"
    # results = config_chain_extraction(top_level)
    moduleConfigOrder = config_chain_extraction(top_level)

    xml_bitstream = f"{design_source_dir}/fabric_independent_bitstream.xml"
    module_info = bitstream_label(moduleConfigOrder, xml_bitstream)

    device_visualization(module_info,moduleConfigOrder)

    # for module in module_info:
    #     print(f"{module} : {len(module_info[module])}")

    # Top Left Window
    target_modules = [
        "sb_0__4_",
        "sb_1__4_",
        "sb_2__4_",
        "sb_0__3_",
        "sb_1__3_",
        "sb_2__3_",
        "sb_0__2_",
        "sb_1__2_",
        "sb_2__2_",
        "grid_clb_1__3_",
        "grid_clb_1__4_",
        "grid_clb_2__3_",
        "grid_clb_2__4_",
        "cbx_1__4_",
        "cbx_1__3_",
        "cbx_1__2_",
        "cbx_2__4_",
        "cbx_2__3_",
        "cbx_2__2_",
        "cby_0__4_",
        "cby_0__3_",
        "cby_1__4_",
        "cby_1__3_",
        "cby_2__4_",
        "cby_2__3_",
    ]
    make_windows(module_info,target_modules)

    # Top Right Window
    target_modules = [
        "sb_2__4_",
        "sb_3__4_",
        "sb_4__4_",
        "sb_2__3_",
        "sb_3__3_",
        "sb_4__3_",
        "sb_2__2_",
        "sb_3__2_",
        "sb_4__2_",
        "grid_clb_3__3_",
        "grid_clb_3__4_",
        "grid_clb_4__3_",
        "grid_clb_4__4_",
        "cbx_4__4_",
        "cbx_4__3_",
        "cbx_4__2_",
        "cbx_3__4_",
        "cbx_3__3_",
        "cbx_3__2_",
        "cby_2__4_",
        "cby_2__3_",
        "cby_3__4_",
        "cby_3__3_",
        "cby_4__4_",
        "cby_4__3_",
    ]
    make_windows(module_info,target_modules)

    # Bottom Left Window
    target_modules = [
        "sb_0__0_",
        "sb_0__1_",
        "sb_0__2_",
        "sb_1__0_",
        "sb_1__1_",
        "sb_1__2_",
        "sb_2__0_",
        "sb_2__1_",
        "sb_2__2_",
        "grid_clb_1__1_",
        "grid_clb_1__2_",
        "grid_clb_2__1_",
        "grid_clb_2__2_",
        "cbx_1__0_",
        "cbx_2__0_",
        "cbx_1__1_",
        "cbx_2__1_",
        "cbx_1__2_",
        "cbx_2__2_",
        "cby_0__1_",
        "cby_0__2_",
        "cby_1__1_",
        "cby_1__2_",
        "cby_2__1_",
        "cby_2__2_",
    ]
    make_windows(module_info,target_modules)

    # Bottom Right Window
    target_modules = [
        "sb_2__0_",
        "sb_2__1_",
        "sb_2__2_",
        "sb_3__0_",
        "sb_3__1_",
        "sb_3__2_",
        "sb_4__0_",
        "sb_4__1_",
        "sb_4__2_",
        "grid_clb_3__1_",
        "grid_clb_3__2_",
        "grid_clb_4__1_",
        "grid_clb_4__2_",
        "cbx_3__0_",
        "cbx_4__0_",
        "cbx_3__1_",
        "cbx_4__1_",
        "cbx_3__2_",
        "cbx_4__2_",
        "cby_2__1_",
        "cby_2__2_",
        "cby_3__1_",
        "cby_3__2_",
        "cby_4__1_",
        "cby_4__2_",
    ]
    make_windows(module_info,target_modules)

if __name__ == "__main__":
    # generate_il_designs()
    # write_task_config()
    # run_task_config(NUM_DESIGNS=5000)

    # 1. Doubled Device Size, Simialar Connections
    # gen_4x4_designs()
    analyze_4x4_designs()

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
    