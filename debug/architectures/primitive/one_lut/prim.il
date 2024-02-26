# Simple Yosys IL file for a single LUT
autoidx 140
attribute \top 1
module \fpga_design
  wire input 4 \lut_in0
  wire input 3 \lut_in1
  wire input 2 \lut_in2
  wire input 1 \lut_in3
  wire output 5 \lut_out
  cell $lut $abc$138$auto$blifparse.cc:525:parse_blif$139
    parameter \LUT 16'0000000000000001
    parameter \WIDTH 4
    connect \A { \lut_in0 \lut_in1 \lut_in3 \lut_in2 }
    connect \Y \lut_out
  end
end
