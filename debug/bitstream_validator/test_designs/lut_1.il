# design #: 00001
# num luts #: 1
autoidx 140
attribute \top 1
module \fpga_design
  wire input 0 \fpga_in_0
  wire input 1 \fpga_in_1
  wire input 2 \fpga_in_2
  wire input 3 \fpga_in_3
  wire output 5 \fpga_out_0
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$0
    parameter \LUT 16'1101110010011001
    parameter \WIDTH 4
    connect \A { \fpga_in_3 \fpga_in_1 \fpga_in_0 \fpga_in_2 }
    connect \Y \fpga_out_0
  end
end
