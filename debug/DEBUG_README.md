# Debug Guide

## Setup
- Source `openfpga.sh`

```
source /home/oshears/Documents/openfpga/OpenFPGA/openfpga.sh
python3 openfpga_flow/scripts/run_fpga_task.py basic_tests/generate_fabric
python3 openfpga_flow/scripts/run_fpga_task.py fpga_verilog/adder/hard_adder
python3 openfpga_flow/tasks/basic_tests/0_debug_task/design_analysis --maxthreads=8 --debug
python3 openfpga_flow/scripts/run_fpga_task.py openfpga_flow/tasks/basic_tests/0_debug_task/fpga_40x40_clb --maxthreads=8 --debug
python3 openfpga_flow/scripts/run_fpga_task.py openfpga_flow/tasks/basic_tests/0_debug_task/openfpga__arch_42x42__tiered_luts__20240516 --maxthreads=8 --debug
python3 openfpga_flow/scripts/run_fpga_task.py openfpga_flow/tasks/basic_tests/0_debug_task/openfpga__arch_42x42__windows_1__partitions_400__tiered_luts__20240517/ --maxthreads=8 --debug

python3 /home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/arch_gen/main_42x42.py && python3 openfpga_flow/scripts/run_fpga_task.py openfpga_flow/tasks/basic_tests/0_debug_task/openfpga__arch_42x42__windows_1__partitions_400__tiered_luts__20240520/ --maxthreads=8
```

---

## Visualize VPR Implementation of a Design (.blif)

```
./build/vtr-verilog-to-routing/vpr/vpr --disp on /home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/k4_N4_tileable_40nm.xml /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/unused_inputs/run002/k4_N4_tileable_40nm/generic_func/MIN_ROUTE_CHAN_WIDTH/generic_func_yosys_out.blif

./build/vtr-verilog-to-routing/vpr/vpr --disp on /home/oshears/Documents/openfpga/OpenFPGA/debug/architectures/k4_N4_tileable_40nm.xml /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/openfpga__arch_42x42__windows_1__partitions_400__tiered_luts__20240517/latest/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/fpga_design_yosys_out.blif
```

---

## Write Netlist JSON
```
/home/oshears/Documents/openfpga/OpenFPGA/build/yosys/bin/yosys /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/full_testbench/configuration_chain/latest/k4_N4_tileable_40nm/and2/MIN_ROUTE_CHAN_WIDTH/yosys.ys
```

## View Netlist
```
netlistsvg -o out.svg /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/full_testbench/configuration_chain/latest/k4_N4_tileable_40nm/and2/MIN_ROUTE_CHAN_WIDTH/and2_yosys_out.json

netlistsvg -o out.svg /home/oshears/Documents/openfpga/OpenFPGA/openfpga_flow/tasks/basic_tests/0_debug_task/openfpga__arch_42x42__windows_1__partitions_400__tiered_luts__20240517/latest/k4_N4_tileable_40nm_new/bench0_fpga_design/MIN_ROUTE_CHAN_WIDTH/fpga_design_yosys_out.blif.json
```

## View Netlist via Yosys
```yosys
read_rtlil ...
show -format svg
/home/oshears/.yosys_show.svg
```

## Simulate Design
```

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

rsync -avzh --progress --stats openfpga__arch_42x42__tiered_luts__20240516.tar.gz  shears@yoda.ads.isi.edu:~/Downloads
```
