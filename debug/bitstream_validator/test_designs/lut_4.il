# design #: 00001
# num luts #: 4
autoidx 140
attribute \top 1
module \fpga_design
  wire input 0 \fpga_in_0
  wire input 1 \fpga_in_1
  wire input 2 \fpga_in_2
  wire input 3 \fpga_in_3
  wire output 5 \fpga_out_0
  wire output 6 \fpga_out_1
  wire output 7 \fpga_out_2
  wire output 8 \fpga_out_3
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$0
    parameter \LUT 16'1101110010011001
    parameter \WIDTH 4
    connect \A { \fpga_in_3 \fpga_in_1 \fpga_in_0 \fpga_in_2 }
    connect \Y \fpga_out_0
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$1
    parameter \LUT 16'0000100111100111
    parameter \WIDTH 4
    connect \A { \fpga_in_0 \fpga_in_2 \fpga_in_3 \fpga_in_1 }
    connect \Y \fpga_out_1
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$2
    parameter \LUT 16'0101111101101011
    parameter \WIDTH 4
    connect \A { \fpga_in_2 \fpga_in_3 \fpga_in_1 \fpga_in_0 }
    connect \Y \fpga_out_2
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$3
    parameter \LUT 16'1101001010110111
    parameter \WIDTH 4
    connect \A { \fpga_in_2 \fpga_in_0 \fpga_in_3 \fpga_in_1 }
    connect \Y \fpga_out_3
  end
end
