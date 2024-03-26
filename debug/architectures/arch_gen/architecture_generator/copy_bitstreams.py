## copy bitstreams script
def copy_bitstreams():
    fh = open("/home/oshears/Documents/openfpga/OpenFPGA/debug/scripts/copy_bitstreams.sh","w+")

    suffix = "_16LUT"
    run_folder = "run003"

    fh.write(f"rm -rf /home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/random_bitstreams{suffix}\n")
    fh.write(f"mkdir /home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/random_bitstreams{suffix}\n")
    for i in range(20000):
        idx = f"{i}".zfill(5)
        fh.write(f"cp /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/random_designs/{run_folder}/k4_N4_tileable_40nm_new/bench{i}_fpga_design/MIN_ROUTE_CHAN_WIDTH/fabric_bitstream.bit /home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/random_bitstreams{suffix}/bitstream_{idx}.bit\n")
        fh.write(f"cp /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/random_designs/{run_folder}/k4_N4_tileable_40nm_new/bench{i}_fpga_design/MIN_ROUTE_CHAN_WIDTH/fabric_independent_bitstream.xml /home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/random_bitstreams{suffix}/bitstream_{idx}.xml\n")
    fh.close()

    # bash /home/oshears/Documents/openfpga/OpenFPGA/debug/scripts/copy_bitstreams.sh