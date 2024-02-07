from xml.etree import ElementTree
import csv
import re

baseDir = "/home/oshears/Documents/openfpga/OpenFPGA"

resultsPath = f"{baseDir}/openfpga_flow/tasks/basic_tests/0_debug_task/random_designs/run014/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH"

bitstreamFile = f"{resultsPath}/fabric_independent_bitstream.xml"


moduleFile = f"{resultsPath}/SRC/routing/sb_0__2_.v"
moduleName = "sb_0__2_"
moduleType = "sb_0__2_"

csvBitstream = f"{baseDir}/debug/bitstream_validator/sample_bitstream.csv"


module_order = [
    "grid_io_bottom_1__0_",
    "grid_io_bottom_2__0_",
    "grid_io_right_3__1_",
    "grid_io_right_3__2_",
    "sb_2__2_",
    "cbx_2__2_",
    "grid_io_top_2__3_",
    "sb_1__2_",
    "cbx_1__2_",
    "grid_io_top_1__3_",
    "sb_0__2_",
    "sb_0__1_",
    "cby_0__2_",
    "grid_io_left_0__2_",
    "sb_0__0_",
    "cby_0__1_",
    "grid_io_left_0__1_",
    "sb_1__0_",
    "cbx_1__0_",
    "cby_1__1_",
    "grid_clb_1__1_",
    "sb_2__0_",
    "cbx_2__0_",
    "cby_2__1_",
    "grid_clb_2__1_",
    "sb_2__1_",
    "cbx_2__1_",
    "cby_2__2_",
    "grid_clb_2__2_",
    "sb_1__1_",
    "cbx_1__1_",
    "cby_1__2_",
    "grid_clb_1__2_"
]
module_order.reverse()