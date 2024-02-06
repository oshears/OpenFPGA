// design #: 00001
// num luts #: 15


`timescale 1ns / 1ps

module fpga_design(fpga_in_0, fpga_in_1, fpga_in_2, fpga_in_3, fpga_out_0, fpga_out_1, fpga_out_2, fpga_out_3, fpga_out_4, fpga_out_5, fpga_out_6, fpga_out_7, fpga_out_8, fpga_out_9, fpga_out_10, fpga_out_11, fpga_out_12, fpga_out_13, fpga_out_14);

input wire fpga_in_0;
input wire fpga_in_1;
input wire fpga_in_2;
input wire fpga_in_3;
output reg fpga_out_0;
output reg fpga_out_1;
output reg fpga_out_2;
output reg fpga_out_3;
output reg fpga_out_4;
output reg fpga_out_5;
output reg fpga_out_6;
output reg fpga_out_7;
output reg fpga_out_8;
output reg fpga_out_9;
output reg fpga_out_10;
output reg fpga_out_11;
output reg fpga_out_12;
output reg fpga_out_13;
output reg fpga_out_14;
// LUT 0 Inputs 
wire lut_0_in_0;
wire lut_0_in_1;
wire lut_0_in_2;
wire lut_0_in_3;
wire lut_0_out;
assign fpga_out_0 = lut_0_out;
assign lut_0_in_0 = fpga_in_0;
assign lut_0_in_1 = fpga_in_0;
assign lut_0_in_2 = fpga_in_0;
assign lut_0_in_3 = fpga_in_2;

// LUT 1 Inputs 
wire lut_1_in_0;
wire lut_1_in_1;
wire lut_1_in_2;
wire lut_1_in_3;
wire lut_1_out;
assign fpga_out_1 = lut_1_out;
assign lut_1_in_0 = fpga_in_1;
assign lut_1_in_1 = fpga_in_0;
assign lut_1_in_2 = fpga_in_0;
assign lut_1_in_3 = fpga_in_1;

// LUT 2 Inputs 
wire lut_2_in_0;
wire lut_2_in_1;
wire lut_2_in_2;
wire lut_2_in_3;
wire lut_2_out;
assign fpga_out_2 = lut_2_out;
assign lut_2_in_0 = fpga_in_0;
assign lut_2_in_1 = fpga_in_3;
assign lut_2_in_2 = fpga_in_0;
assign lut_2_in_3 = fpga_in_2;

// LUT 3 Inputs 
wire lut_3_in_0;
wire lut_3_in_1;
wire lut_3_in_2;
wire lut_3_in_3;
wire lut_3_out;
assign fpga_out_3 = lut_3_out;
assign lut_3_in_0 = fpga_in_2;
assign lut_3_in_1 = fpga_in_2;
assign lut_3_in_2 = fpga_in_0;
assign lut_3_in_3 = fpga_in_3;

// LUT 4 Inputs 
wire lut_4_in_0;
wire lut_4_in_1;
wire lut_4_in_2;
wire lut_4_in_3;
wire lut_4_out;
assign fpga_out_4 = lut_4_out;
assign lut_4_in_0 = fpga_in_0;
assign lut_4_in_1 = fpga_in_0;
assign lut_4_in_2 = fpga_in_1;
assign lut_4_in_3 = fpga_in_2;

// LUT 5 Inputs 
wire lut_5_in_0;
wire lut_5_in_1;
wire lut_5_in_2;
wire lut_5_in_3;
wire lut_5_out;
assign fpga_out_5 = lut_5_out;
assign lut_5_in_0 = fpga_in_2;
assign lut_5_in_1 = fpga_in_1;
assign lut_5_in_2 = fpga_in_2;
assign lut_5_in_3 = fpga_in_1;

// LUT 6 Inputs 
wire lut_6_in_0;
wire lut_6_in_1;
wire lut_6_in_2;
wire lut_6_in_3;
wire lut_6_out;
assign fpga_out_6 = lut_6_out;
assign lut_6_in_0 = fpga_in_3;
assign lut_6_in_1 = fpga_in_2;
assign lut_6_in_2 = fpga_in_1;
assign lut_6_in_3 = fpga_in_0;

// LUT 7 Inputs 
wire lut_7_in_0;
wire lut_7_in_1;
wire lut_7_in_2;
wire lut_7_in_3;
wire lut_7_out;
assign fpga_out_7 = lut_7_out;
assign lut_7_in_0 = fpga_in_2;
assign lut_7_in_1 = fpga_in_3;
assign lut_7_in_2 = fpga_in_1;
assign lut_7_in_3 = fpga_in_2;

// LUT 8 Inputs 
wire lut_8_in_0;
wire lut_8_in_1;
wire lut_8_in_2;
wire lut_8_in_3;
wire lut_8_out;
assign fpga_out_8 = lut_8_out;
assign lut_8_in_0 = fpga_in_2;
assign lut_8_in_1 = fpga_in_2;
assign lut_8_in_2 = fpga_in_1;
assign lut_8_in_3 = fpga_in_1;

// LUT 9 Inputs 
wire lut_9_in_0;
wire lut_9_in_1;
wire lut_9_in_2;
wire lut_9_in_3;
wire lut_9_out;
assign fpga_out_9 = lut_9_out;
assign lut_9_in_0 = fpga_in_3;
assign lut_9_in_1 = fpga_in_0;
assign lut_9_in_2 = fpga_in_1;
assign lut_9_in_3 = fpga_in_3;

// LUT 10 Inputs 
wire lut_10_in_0;
wire lut_10_in_1;
wire lut_10_in_2;
wire lut_10_in_3;
wire lut_10_out;
assign fpga_out_10 = lut_10_out;
assign lut_10_in_0 = fpga_in_3;
assign lut_10_in_1 = fpga_in_0;
assign lut_10_in_2 = fpga_in_2;
assign lut_10_in_3 = fpga_in_3;

// LUT 11 Inputs 
wire lut_11_in_0;
wire lut_11_in_1;
wire lut_11_in_2;
wire lut_11_in_3;
wire lut_11_out;
assign fpga_out_11 = lut_11_out;
assign lut_11_in_0 = fpga_in_1;
assign lut_11_in_1 = fpga_in_3;
assign lut_11_in_2 = fpga_in_0;
assign lut_11_in_3 = fpga_in_1;

// LUT 12 Inputs 
wire lut_12_in_0;
wire lut_12_in_1;
wire lut_12_in_2;
wire lut_12_in_3;
wire lut_12_out;
assign fpga_out_12 = lut_12_out;
assign lut_12_in_0 = fpga_in_2;
assign lut_12_in_1 = fpga_in_0;
assign lut_12_in_2 = fpga_in_2;
assign lut_12_in_3 = fpga_in_1;

// LUT 13 Inputs 
wire lut_13_in_0;
wire lut_13_in_1;
wire lut_13_in_2;
wire lut_13_in_3;
wire lut_13_out;
assign fpga_out_13 = lut_13_out;
assign lut_13_in_0 = fpga_in_0;
assign lut_13_in_1 = fpga_in_1;
assign lut_13_in_2 = fpga_in_3;
assign lut_13_in_3 = fpga_in_1;

// LUT 14 Inputs 
wire lut_14_in_0;
wire lut_14_in_1;
wire lut_14_in_2;
wire lut_14_in_3;
wire lut_14_out;
assign fpga_out_14 = lut_14_out;
assign lut_14_in_0 = fpga_in_3;
assign lut_14_in_1 = fpga_in_1;
assign lut_14_in_2 = fpga_in_2;
assign lut_14_in_3 = fpga_in_0;


always @(*) begin
	case ({lut_0_in_3, lut_0_in_2, lut_0_in_1, lut_0_in_0})
		4'b0000: lut_0_out <= 1;
		4'b0001: lut_0_out <= 0;
		4'b0010: lut_0_out <= 0;
		4'b0011: lut_0_out <= 0;
		4'b0100: lut_0_out <= 1;
		4'b0101: lut_0_out <= 0;
		4'b0110: lut_0_out <= 0;
		4'b0111: lut_0_out <= 1;
		4'b1000: lut_0_out <= 1;
		4'b1001: lut_0_out <= 0;
		4'b1010: lut_0_out <= 1;
		4'b1011: lut_0_out <= 1;
		4'b1100: lut_0_out <= 0;
		4'b1101: lut_0_out <= 1;
		4'b1110: lut_0_out <= 0;
		4'b1111: lut_0_out <= 1;
		default: lut_0_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_1_in_3, lut_1_in_2, lut_1_in_1, lut_1_in_0})
		4'b0000: lut_1_out <= 0;
		4'b0001: lut_1_out <= 1;
		4'b0010: lut_1_out <= 1;
		4'b0011: lut_1_out <= 0;
		4'b0100: lut_1_out <= 0;
		4'b0101: lut_1_out <= 1;
		4'b0110: lut_1_out <= 0;
		4'b0111: lut_1_out <= 1;
		4'b1000: lut_1_out <= 0;
		4'b1001: lut_1_out <= 0;
		4'b1010: lut_1_out <= 0;
		4'b1011: lut_1_out <= 1;
		4'b1100: lut_1_out <= 1;
		4'b1101: lut_1_out <= 1;
		4'b1110: lut_1_out <= 1;
		4'b1111: lut_1_out <= 1;
		default: lut_1_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_2_in_3, lut_2_in_2, lut_2_in_1, lut_2_in_0})
		4'b0000: lut_2_out <= 1;
		4'b0001: lut_2_out <= 0;
		4'b0010: lut_2_out <= 0;
		4'b0011: lut_2_out <= 0;
		4'b0100: lut_2_out <= 1;
		4'b0101: lut_2_out <= 0;
		4'b0110: lut_2_out <= 0;
		4'b0111: lut_2_out <= 0;
		4'b1000: lut_2_out <= 0;
		4'b1001: lut_2_out <= 0;
		4'b1010: lut_2_out <= 0;
		4'b1011: lut_2_out <= 1;
		4'b1100: lut_2_out <= 1;
		4'b1101: lut_2_out <= 1;
		4'b1110: lut_2_out <= 0;
		4'b1111: lut_2_out <= 1;
		default: lut_2_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_3_in_3, lut_3_in_2, lut_3_in_1, lut_3_in_0})
		4'b0000: lut_3_out <= 1;
		4'b0001: lut_3_out <= 0;
		4'b0010: lut_3_out <= 0;
		4'b0011: lut_3_out <= 0;
		4'b0100: lut_3_out <= 1;
		4'b0101: lut_3_out <= 1;
		4'b0110: lut_3_out <= 1;
		4'b0111: lut_3_out <= 0;
		4'b1000: lut_3_out <= 1;
		4'b1001: lut_3_out <= 0;
		4'b1010: lut_3_out <= 1;
		4'b1011: lut_3_out <= 0;
		4'b1100: lut_3_out <= 1;
		4'b1101: lut_3_out <= 0;
		4'b1110: lut_3_out <= 0;
		4'b1111: lut_3_out <= 0;
		default: lut_3_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_4_in_3, lut_4_in_2, lut_4_in_1, lut_4_in_0})
		4'b0000: lut_4_out <= 0;
		4'b0001: lut_4_out <= 1;
		4'b0010: lut_4_out <= 1;
		4'b0011: lut_4_out <= 0;
		4'b0100: lut_4_out <= 1;
		4'b0101: lut_4_out <= 0;
		4'b0110: lut_4_out <= 0;
		4'b0111: lut_4_out <= 0;
		4'b1000: lut_4_out <= 1;
		4'b1001: lut_4_out <= 1;
		4'b1010: lut_4_out <= 1;
		4'b1011: lut_4_out <= 0;
		4'b1100: lut_4_out <= 1;
		4'b1101: lut_4_out <= 0;
		4'b1110: lut_4_out <= 1;
		4'b1111: lut_4_out <= 0;
		default: lut_4_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_5_in_3, lut_5_in_2, lut_5_in_1, lut_5_in_0})
		4'b0000: lut_5_out <= 1;
		4'b0001: lut_5_out <= 0;
		4'b0010: lut_5_out <= 1;
		4'b0011: lut_5_out <= 1;
		4'b0100: lut_5_out <= 0;
		4'b0101: lut_5_out <= 1;
		4'b0110: lut_5_out <= 1;
		4'b0111: lut_5_out <= 0;
		4'b1000: lut_5_out <= 0;
		4'b1001: lut_5_out <= 0;
		4'b1010: lut_5_out <= 0;
		4'b1011: lut_5_out <= 1;
		4'b1100: lut_5_out <= 1;
		4'b1101: lut_5_out <= 0;
		4'b1110: lut_5_out <= 0;
		4'b1111: lut_5_out <= 0;
		default: lut_5_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_6_in_3, lut_6_in_2, lut_6_in_1, lut_6_in_0})
		4'b0000: lut_6_out <= 0;
		4'b0001: lut_6_out <= 0;
		4'b0010: lut_6_out <= 1;
		4'b0011: lut_6_out <= 1;
		4'b0100: lut_6_out <= 0;
		4'b0101: lut_6_out <= 0;
		4'b0110: lut_6_out <= 1;
		4'b0111: lut_6_out <= 0;
		4'b1000: lut_6_out <= 0;
		4'b1001: lut_6_out <= 1;
		4'b1010: lut_6_out <= 1;
		4'b1011: lut_6_out <= 0;
		4'b1100: lut_6_out <= 1;
		4'b1101: lut_6_out <= 0;
		4'b1110: lut_6_out <= 0;
		4'b1111: lut_6_out <= 0;
		default: lut_6_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_7_in_3, lut_7_in_2, lut_7_in_1, lut_7_in_0})
		4'b0000: lut_7_out <= 0;
		4'b0001: lut_7_out <= 1;
		4'b0010: lut_7_out <= 0;
		4'b0011: lut_7_out <= 1;
		4'b0100: lut_7_out <= 1;
		4'b0101: lut_7_out <= 0;
		4'b0110: lut_7_out <= 1;
		4'b0111: lut_7_out <= 0;
		4'b1000: lut_7_out <= 0;
		4'b1001: lut_7_out <= 0;
		4'b1010: lut_7_out <= 0;
		4'b1011: lut_7_out <= 1;
		4'b1100: lut_7_out <= 0;
		4'b1101: lut_7_out <= 1;
		4'b1110: lut_7_out <= 1;
		4'b1111: lut_7_out <= 1;
		default: lut_7_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_8_in_3, lut_8_in_2, lut_8_in_1, lut_8_in_0})
		4'b0000: lut_8_out <= 1;
		4'b0001: lut_8_out <= 0;
		4'b0010: lut_8_out <= 0;
		4'b0011: lut_8_out <= 1;
		4'b0100: lut_8_out <= 0;
		4'b0101: lut_8_out <= 0;
		4'b0110: lut_8_out <= 1;
		4'b0111: lut_8_out <= 0;
		4'b1000: lut_8_out <= 1;
		4'b1001: lut_8_out <= 0;
		4'b1010: lut_8_out <= 1;
		4'b1011: lut_8_out <= 1;
		4'b1100: lut_8_out <= 0;
		4'b1101: lut_8_out <= 1;
		4'b1110: lut_8_out <= 0;
		4'b1111: lut_8_out <= 0;
		default: lut_8_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_9_in_3, lut_9_in_2, lut_9_in_1, lut_9_in_0})
		4'b0000: lut_9_out <= 0;
		4'b0001: lut_9_out <= 1;
		4'b0010: lut_9_out <= 1;
		4'b0011: lut_9_out <= 0;
		4'b0100: lut_9_out <= 0;
		4'b0101: lut_9_out <= 1;
		4'b0110: lut_9_out <= 1;
		4'b0111: lut_9_out <= 1;
		4'b1000: lut_9_out <= 0;
		4'b1001: lut_9_out <= 1;
		4'b1010: lut_9_out <= 0;
		4'b1011: lut_9_out <= 1;
		4'b1100: lut_9_out <= 1;
		4'b1101: lut_9_out <= 1;
		4'b1110: lut_9_out <= 1;
		4'b1111: lut_9_out <= 0;
		default: lut_9_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_10_in_3, lut_10_in_2, lut_10_in_1, lut_10_in_0})
		4'b0000: lut_10_out <= 0;
		4'b0001: lut_10_out <= 0;
		4'b0010: lut_10_out <= 1;
		4'b0011: lut_10_out <= 1;
		4'b0100: lut_10_out <= 0;
		4'b0101: lut_10_out <= 1;
		4'b0110: lut_10_out <= 0;
		4'b0111: lut_10_out <= 1;
		4'b1000: lut_10_out <= 0;
		4'b1001: lut_10_out <= 0;
		4'b1010: lut_10_out <= 1;
		4'b1011: lut_10_out <= 0;
		4'b1100: lut_10_out <= 0;
		4'b1101: lut_10_out <= 0;
		4'b1110: lut_10_out <= 1;
		4'b1111: lut_10_out <= 0;
		default: lut_10_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_11_in_3, lut_11_in_2, lut_11_in_1, lut_11_in_0})
		4'b0000: lut_11_out <= 1;
		4'b0001: lut_11_out <= 0;
		4'b0010: lut_11_out <= 1;
		4'b0011: lut_11_out <= 0;
		4'b0100: lut_11_out <= 0;
		4'b0101: lut_11_out <= 1;
		4'b0110: lut_11_out <= 0;
		4'b0111: lut_11_out <= 0;
		4'b1000: lut_11_out <= 0;
		4'b1001: lut_11_out <= 0;
		4'b1010: lut_11_out <= 0;
		4'b1011: lut_11_out <= 0;
		4'b1100: lut_11_out <= 0;
		4'b1101: lut_11_out <= 1;
		4'b1110: lut_11_out <= 1;
		4'b1111: lut_11_out <= 1;
		default: lut_11_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_12_in_3, lut_12_in_2, lut_12_in_1, lut_12_in_0})
		4'b0000: lut_12_out <= 1;
		4'b0001: lut_12_out <= 0;
		4'b0010: lut_12_out <= 1;
		4'b0011: lut_12_out <= 1;
		4'b0100: lut_12_out <= 1;
		4'b0101: lut_12_out <= 0;
		4'b0110: lut_12_out <= 1;
		4'b0111: lut_12_out <= 1;
		4'b1000: lut_12_out <= 0;
		4'b1001: lut_12_out <= 0;
		4'b1010: lut_12_out <= 1;
		4'b1011: lut_12_out <= 0;
		4'b1100: lut_12_out <= 0;
		4'b1101: lut_12_out <= 1;
		4'b1110: lut_12_out <= 1;
		4'b1111: lut_12_out <= 0;
		default: lut_12_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_13_in_3, lut_13_in_2, lut_13_in_1, lut_13_in_0})
		4'b0000: lut_13_out <= 1;
		4'b0001: lut_13_out <= 1;
		4'b0010: lut_13_out <= 1;
		4'b0011: lut_13_out <= 0;
		4'b0100: lut_13_out <= 1;
		4'b0101: lut_13_out <= 1;
		4'b0110: lut_13_out <= 0;
		4'b0111: lut_13_out <= 0;
		4'b1000: lut_13_out <= 1;
		4'b1001: lut_13_out <= 0;
		4'b1010: lut_13_out <= 1;
		4'b1011: lut_13_out <= 1;
		4'b1100: lut_13_out <= 0;
		4'b1101: lut_13_out <= 1;
		4'b1110: lut_13_out <= 1;
		4'b1111: lut_13_out <= 1;
		default: lut_13_out <= 0;
	endcase
end

always @(*) begin
	case ({lut_14_in_3, lut_14_in_2, lut_14_in_1, lut_14_in_0})
		4'b0000: lut_14_out <= 1;
		4'b0001: lut_14_out <= 0;
		4'b0010: lut_14_out <= 1;
		4'b0011: lut_14_out <= 0;
		4'b0100: lut_14_out <= 1;
		4'b0101: lut_14_out <= 0;
		4'b0110: lut_14_out <= 0;
		4'b0111: lut_14_out <= 0;
		4'b1000: lut_14_out <= 0;
		4'b1001: lut_14_out <= 1;
		4'b1010: lut_14_out <= 1;
		4'b1011: lut_14_out <= 0;
		4'b1100: lut_14_out <= 0;
		4'b1101: lut_14_out <= 1;
		4'b1110: lut_14_out <= 1;
		4'b1111: lut_14_out <= 1;
		default: lut_14_out <= 0;
	endcase
end
endmodule
