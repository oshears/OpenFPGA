# Debug Guide

## Setup
- Source `openfpga.sh`

```
source /home/oshears/Documents/openfpga/OpenFPGA/openfpga.sh
python3 openfpga_flow/scripts/run_fpga_task.py basic_tests/generate_fabric
```

---

## Visualize VPR Architecture

```
./build/vtr-verilog-to-routing/vpr/vpr --disp on /home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/k4_N4_tileable_40nm.xml /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/unused_inputs/run002/k4_N4_tileable_40nm/generic_func/MIN_ROUTE_CHAN_WIDTH/generic_func_yosys_out.blif
```

---

## Write Netlist JSON
```
/home/oshears/Documents/openfpga/OpenFPGA/build/yosys/bin/yosys /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/full_testbench/configuration_chain/latest/k4_N4_tileable_40nm/and2/MIN_ROUTE_CHAN_WIDTH/yosys.ys
```

## View Netlist
```
netlistsvg -o out.svg /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/full_testbench/configuration_chain/latest/k4_N4_tileable_40nm/and2/MIN_ROUTE_CHAN_WIDTH/and2_yosys_out.json
```


---

## Write Netlist as JSON

```
/home/oshears/Documents/openfpga/OpenFPGA/build/yosys/bin/yosys /home/oshears/Documents/openfpga/OpenFPGA/debug/scripts/compile_design.ys 
```


## View Netlist
```
netlistsvg -o out.svg /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/full_testbench/configuration_chain/latest/k4_N4_tileable_40nm/and2/MIN_ROUTE_CHAN_WIDTH/fpga_top.json
```

---

## Manual Debug
```
source /home/oshears/Documents/openfpga/OpenFPGA/openfpga.sh
python3 openfpga_flow/scripts/run_fpga_task.py basic_tests/0_debug_task/unused_inputs
```

---

## Random Designs
```
python3 openfpga_flow/scripts/run_fpga_task.py basic_tests/0_debug_task/random_designs --maxthreads=8 --debug

rm -rf /home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/random_bitstreams/*.csv

tar -czvf bitstreams.tar.gz random_bitstreams/
```