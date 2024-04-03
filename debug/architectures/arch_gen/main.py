# import sys
# sys.path.append('/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/scripts')

from architecture_generator.copy_bitstreams import *
from architecture_generator.gen_designs import *
from architecture_generator.task_config import *

import os

# from openfpga_flow.scripts.run_fpga_task.py
# from run_fpga_task import main



if __name__ == "__main__":
    # generate_il_designs()
    # write_task_config()
    # run_task_config()

    # python3 openfpga_flow/scripts/run_fpga_task.py openfpga_flow/tasks/basic_tests/0_debug_task/design_analysis --maxthreads 10
    cmd = ""
    cmd += "cd /home/oshears/Documents/openfpga/OpenFPGA/ && bash openfpga.sh"
    cmd += "python3 openfpga_flow/scripts/run_fpga_task.py "
    cmd += "openfpga_flow/tasks/basic_tests/0_debug_task/design_analysis "
    # cmd += "--maxthreads 10 "
    # cmd += "--debug "

    # NOTE: Do I need to run open_fpga.sh before launching this task?
    os.system(cmd)
    # if result != 0:
    #     print("THE TEST FAILED!")


    # copy_bitstreams()
    