`timescale 1ns / 1ps

module generic_func(lut_in3, lut_in2, lut_in1, lut_in0, lut_out);

input wire lut_in0;
input wire lut_in1;
input wire lut_in2;
input wire lut_in3;
output reg lut_out;

always @(*) begin
	case ({lut_in3, lut_in2, lut_in1, lut_in0})
		4'b0000: lut_out <= 0;
		4'b0001: lut_out <= 0;
		4'b0010: lut_out <= 0;
		4'b0011: lut_out <= 0;
		4'b0100: lut_out <= 0;
		4'b0101: lut_out <= 0;
		4'b0110: lut_out <= 0;
		4'b0111: lut_out <= 0;
		4'b1000: lut_out <= 0;
		4'b1001: lut_out <= 0;
		4'b1010: lut_out <= 0;
		4'b1011: lut_out <= 0;
		4'b1100: lut_out <= 0;
		4'b1101: lut_out <= 0;
		4'b1110: lut_out <= 0;
		4'b1111: lut_out <= 0;
		default: lut_out <= 0;
	endcase
end
endmodule
