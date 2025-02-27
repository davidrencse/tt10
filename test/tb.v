`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();
   // Inputs
  reg [7:0] ui_in;   // A
  reg [7:0] uio_in;  // B
  reg clk;
  reg rst_n;
  // Replace tt_um_example with your module name:
  tt10 user_project (
    .ui_in(ui_in),
    .uio_in(uio_in),
    .uo_out(uo_out),
    .clk(clk),
    .rst_n(rst_n)
  );

  // Generate a 10us clock (100 KHz)
  initial begin
    clk = 0;
    forever #5 clk = ~clk; // 10us period (100 KHz)
  end

  // Initialize VCD waveform dumping
  initial begin
    $dumpfile("test.vcd");
    $dumpvars(0, tb); // Dump all signals in the testbench
  end

  // Test sequence
  initial begin
    // Initialize inputs and reset
    ui_in = 8'b0;
    uio_in = 8'b0;
    rst_n = 0; // Assert reset (active low)

    // Release reset after 20ns
    #20;
    rst_n = 1;

    // Test case 1: A[7] = 0 (no shift)
    ui_in = 8'b01010101; // 0x55
    uio_in = 8'b00110011; // 0x33
    #20; // Wait 20ns
    $display("Test 1: C = %b (Expected: 01100110)", uo_out);
    if (uo_out !== 8'b01100110) $error("Test 1 failed!");

    // Test case 2: A[7] = 1 (shift left)
    ui_in = 8'b11010101; // 0xD5
    uio_in = 8'b00110011; // 0x33
    #20;
    $display("Test 2: C = %b (Expected: 11001100)", uo_out);
    if (uo_out !== 8'b11001100) $error("Test 2 failed!");

    // Test case 3: A = B (XOR = 0)
    ui_in = 8'b11111111; // 0xFF
    uio_in = 8'b11111111; // 0xFF
    #20;
    $display("Test 3: C = %b (Expected: 00000000)", uo_out);
    if (uo_out !== 8'b00000000) $error("Test 3 failed!");

    // Finish simulation
    $finish;
  end

endmodule
