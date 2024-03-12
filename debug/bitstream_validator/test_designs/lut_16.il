# design #: 00001
# num luts #: 16
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
  wire output 9 \fpga_out_4
  wire output 10 \fpga_out_5
  wire output 11 \fpga_out_6
  wire output 12 \fpga_out_7
  wire output 13 \fpga_out_8
  wire output 14 \fpga_out_9
  wire output 15 \fpga_out_10
  wire output 16 \fpga_out_11
  wire output 17 \fpga_out_12
  wire output 18 \fpga_out_13
  wire output 19 \fpga_out_14
  wire output 20 \fpga_out_15
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
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$4
    parameter \LUT 16'1011101100101110
    parameter \WIDTH 4
    connect \A { \fpga_in_1 \fpga_in_0 \fpga_in_2 \fpga_in_3 }
    connect \Y \fpga_out_4
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$5
    parameter \LUT 16'1100100110111110
    parameter \WIDTH 4
    connect \A { \fpga_in_0 \fpga_in_3 \fpga_in_2 \fpga_in_1 }
    connect \Y \fpga_out_5
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$6
    parameter \LUT 16'1111111111000100
    parameter \WIDTH 4
    connect \A { \fpga_in_0 \fpga_in_2 \fpga_in_3 \fpga_in_1 }
    connect \Y \fpga_out_6
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$7
    parameter \LUT 16'0110100000110000
    parameter \WIDTH 4
    connect \A { \fpga_in_1 \fpga_in_0 \fpga_in_3 \fpga_in_2 }
    connect \Y \fpga_out_7
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$8
    parameter \LUT 16'1100001101101100
    parameter \WIDTH 4
    connect \A { \fpga_in_0 \fpga_in_3 \fpga_in_2 \fpga_in_1 }
    connect \Y \fpga_out_8
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$9
    parameter \LUT 16'0011111110101010
    parameter \WIDTH 4
    connect \A { \fpga_in_2 \fpga_in_1 \fpga_in_3 \fpga_in_0 }
    connect \Y \fpga_out_9
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$10
    parameter \LUT 16'0011011001100000
    parameter \WIDTH 4
    connect \A { \fpga_in_2 \fpga_in_0 \fpga_in_3 \fpga_in_1 }
    connect \Y \fpga_out_10
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$11
    parameter \LUT 16'1011101111000011
    parameter \WIDTH 4
    connect \A { \fpga_in_1 \fpga_in_3 \fpga_in_0 \fpga_in_2 }
    connect \Y \fpga_out_11
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$12
    parameter \LUT 16'1100000010110101
    parameter \WIDTH 4
    connect \A { \fpga_in_2 \fpga_in_1 \fpga_in_0 \fpga_in_3 }
    connect \Y \fpga_out_12
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$13
    parameter \LUT 16'1100011010101011
    parameter \WIDTH 4
    connect \A { \fpga_in_2 \fpga_in_1 \fpga_in_3 \fpga_in_0 }
    connect \Y \fpga_out_13
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$14
    parameter \LUT 16'1100110000110000
    parameter \WIDTH 4
    connect \A { \fpga_in_2 \fpga_in_3 \fpga_in_1 \fpga_in_0 }
    connect \Y \fpga_out_14
  end
  cell $lut $abc$963$auto$blifparse.cc:525:parse_blif$15
    parameter \LUT 16'1100011011000000
    parameter \WIDTH 4
    connect \A { \fpga_in_3 \fpga_in_2 \fpga_in_1 \fpga_in_0 }
    connect \Y \fpga_out_15
  end
end
