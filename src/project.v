/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt10 (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

   wire [7:0] xor_result = ui_in ^ uio_in;

  // Conditional shift logic
  reg [7:0] c_out;
  always @(*) begin
    if (!rst_n) begin
      c_out = 8'b0;  // Reset to 0
    end else begin
      c_out = ui_in[7] ? {xor_result[6:0], 1'b0} : xor_result;
    end
  end

  assign uo_out = c_out;

endmodule
