# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    # Test case 1: A[7] = 0, no shift
    dut.ui_in.value = 0b01010101  # A = 85
    dut.uio_in.value = 0b00110011  # B = 51
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b01100110, f"Expected 102, got {dut.uo_out.value}"

    # Test case 2: A[7] = 1, shift left by 1
    dut.ui_in.value = 0b11010101  # A = 213
    dut.uio_in.value = 0b00110011  # B = 51
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b11001100, f"Expected 204, got {dut.uo_out.value}"

    # Test case 3: A = B, XOR result is 0
    dut.ui_in.value = 0b11111111  # A = 255
    dut.uio_in.value = 0b11111111  # B = 255
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00000000, f"Expected 0, got {dut.uo_out.value}"

    # Test case 4: A = 0, B = 0xFF
    dut.ui_in.value = 0b00000000  # A = 0
    dut.uio_in.value = 0b11111111  # B = 255
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b11111111, f"Expected 255, got {dut.uo_out.value}"

    # Test case 5: A = 0xFF, B = 0x00, A[7] = 1, shift left
    dut.ui_in.value = 0b11111111  # A = 255
    dut.uio_in.value = 0b00000000  # B = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b11111110, f"Expected 254, got {dut.uo_out.value}"

    dut._log.info("All test cases passed")
