from module_pkg.module_classes import *
from module_pkg.fpga_top_parse import *
from module_pkg.map_muxes import *
from module_pkg.parse_verilog_modules import *
from module_pkg.get_bitstream_modules import *
from module_pkg.follow_route import *
from module_pkg.graph_json import *
from module_pkg.trace_paths import *
from module_pkg.dead_ends import *
from module_pkg.display_routes import *
from module_pkg.generate_annotated_bitstream import *
from module_pkg.config_chain_extraction import *

from module_pkg.bitstream_analysis.distribtuions import *

from module_pkg.windows_4x4 import *

# def hasSinglePathPreceedingMux(root:IO, outFile):
    
#     # does this node have a previous driving IO
#     if root.hasPrevIO():
        
#         # if none of the previous driving IO are direct wire connections 
#         # and if the current port is not part of a "grid_io" module
#         if (True not in root.previoIsDirect) and ("grid_io" not in root.moduleName):
            
#             # for each prevIO that is presumably a MUX
#             for prevIO in root.prevIO:
                
#                 # if the mux has multiple options, then it could just be driving something else
#                 # if the mux has one option, then it must be driving this chain
#                 if len(prevIO.nextIO) == 1:
                    
#                     outFile.write(f"\tPossible Single Path Preceeding Mux: {prevIO}\n")
                    
#             return True
#         else:
#             for prevIO in root.prevIO:
#                 return hasSinglePathPreceedingMux(prevIO,outFile)
#     else:
#         return False

# def reportHasSink(root:IO,outFile,pathLength=0):
    
#     for nextIO in root.nextIO:
#         reportHasSink(nextIO, outFile, pathLength + 1)

#     # if not root.hasNextIO() and ("GPIO_PAD" not in root.name) and (root.direction == "output"):

#     # if the port does not have a next and is not a GPIO_PAD, it might be a dead end
#     if not root.hasNextIO() and ("GPIO_PAD" not in root.name):
#         # check to see if it had something leading to it, otherwise we disqualify it
#         # if root.hasPrevIO():
#         # if it had something leading to it, make sure it wasn't just a wire connections (i.e., it was intentionally routed)
#         # if not root.previoIsDirect[0]:
        
#         if "grid_clb" not in root.prevIO[0].moduleName: # TODO: DEBUG: Remove when finished implementing CLB stuff
#             if hasSinglePathPreceedingMux(root, outFile):
#                 outFile.write(f"L={pathLength}, {root.prevIO[0]}\n")


def standard_flow(VERTICAL_CLB_COUNT):
    baseDir = "/home/oshears/Documents/openfpga/OpenFPGA"
    # resultsPath = f"{baseDir}/openfpga_flow/tasks/basic_tests/0_debug_task/random_designs/run003/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
    # resultsPath = f"{baseDir}/openfpga_flow/tasks/basic_tests/0_debug_task/design_analysis/latest/k4_N4_tileable_40nm_new/fpga_design/MIN_ROUTE_CHAN_WIDTH"
    SIZE = f"{VERTICAL_CLB_COUNT}x{VERTICAL_CLB_COUNT}"
    results_dir = f"openfpga_flow/tasks/basic_tests/0_debug_task/fpga_{SIZE}_clb/latest/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"
    bitstreamFile = f"{results_dir}/fabric_independent_bitstream.xml"

    module_order = config_chain_extraction(f"{results_dir}/SRC/fpga_top.v")

    modules:dict[str, Module] = getModules(baseDir, bitstreamFile, module_order=module_order)

    # Identify all of the modules being used (from the top level, per the information from the bitstream)
    parseModules(baseDir, results_dir)

    ## Use information from the bitstreams to determine the mux configurations, and thus the internal routes being used
    ## mapMuxes(baseDir, modules)

    # # Connect the modules per the information from fpga_top.v
    # parseTop(modules, results_dir)

    # # write the routes being actively used out to files
    # displayRoutes(modules)

    # # trace paths from outputs back to their inputs
    # tracePaths(modules)

    # # print dead ends
    # printDeadEnds(modules)

    # create a .csv file with bit annotations
    genNewBitstreams(modules, module_order, out_filename="mappings.csv")

    for window_idx in range(len(windows_4x4)):
        genNewBitstreams(modules, module_order, windows_4x4[window_idx], f"window{window_idx}_mappings.csv")

    # follow_route_for(modules)

def get_distributions():
    # get_config_distributions("/home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/random_designs/run003/k4_N4_tileable_40nm_new")
    bit_reference="debug/bitstream_validator/sample_results/out.csv"
    bitstreams_path="/home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/random_bitstreams_16LUT"
    out_file_path="debug/bitstream_validator/results/bit_config_distributions"
    get_config_distributions(bit_reference, bitstreams_path, out_file_path) 

def visualization_test(config_distributions):
    config_elem = "grid_clb_1__2_.logical_tile_clb_mode_clb__0.logical_tile_clb_mode_default__fle_0.logical_tile_clb_mode_default__fle_mode_n1_lut4__ble4_0.logical_tile_clb_mode_default__fle_mode_n1_lut4__ble4_mode_default__lut4_0.lut4_DFF_mem"
    # config_elem = "cbx_1__0_.mem_bottom_ipin_0"
    config_distribution = config_distributions[config_elem]
    out_file_path = "debug/bitstream_validator/results/bit_config_distributions/graphs"
    
    if len(config_distribution['configs']) < 64:
        write_visualization(config_elem, config_distribution, out_file_path)
    else:
        write_line_graph(config_elem, config_distribution, out_file_path)

def load_distributions():
    pkl_file = "debug/bitstream_validator/results/bit_config_distributions/config_distributions.pkl"
    return load_config_distributions(pkl_file)

def write_all_visualizations(config_distributions):
    
    out_file_path = "debug/bitstream_validator/results/bit_config_distributions/graphs"
    
    write_visualizations(config_distributions,out_file_path)

if __name__ == "__main__":
    standard_flow(4)
    # get_distributions()
    # config_distributions = load_distributions()
    # write_visualizations(config_distributions)