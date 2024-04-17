# import sys
# sys.path.append('/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/scripts')

from architecture_generator.copy_bitstreams import *
from architecture_generator.gen_designs import *
from architecture_generator.task_config import *

import os

# from openfpga_flow.scripts.run_fpga_task.py
# from run_fpga_task import main

def gen_4x4_designs(NUM_DESIGNS=5000):
    # generate_il_designs(5000, NUM_LUTS=64, outdir="fpga_4x4_clb")
    # write_task_config(5000,"4x4", device_arch="")


    NUM_LUTS = 64
    # generate_il_designs(NUM_DESIGNS, NUM_LUTS=NUM_LUTS, outdir="fpga_4x4_clb")
    write_task_config(NUM_DESIGNS, "4x4", outdir="fpga_4x4_clb", bench_dir="debug/architectures/arch_gen/results/fpga_4x4_clb")
    shutil.copy("debug/architectures/arch_gen/results/fpga_4x4_clb/task.conf","openfpga_flow/tasks/basic_tests/0_debug_task/fpga_4x4_clb/config/task.conf")
    
    # run_task_config()

    # python3 openfpga_flow/scripts/run_fpga_task.py basic_tests/0_debug_task/fpga_4x4_clb


if __name__ == "__main__":
    # generate_il_designs()
    # write_task_config()
    # run_task_config(NUM_DESIGNS=5000)

    # 1. Doubled Device Size, Simialar Connections
    gen_4x4_designs()

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
    