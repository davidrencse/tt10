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
    dut.ena.value = 1  # Enable the design
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0  # Active low reset
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1  # Release reset

    dut._log.info("Test project behavior")

    # Test case 1: A[7] = 0 (no shift)
    dut.ui_in.value = 0b01010101  # 0x55
    dut.uio_in.value = 0b00110011  # 0x33
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b01100110, f"Test 1 failed: Expected 01100110, got {dut.uo_out.value}"

    # Test case 2: A[7] = 1 (shift left)
    dut.ui_in.value = 0b11010101  # 0xD5
    dut.uio_in.value = 0b00110011  # 0x33
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b11001100, f"Test 2 failed: Expected 11001100, got {dut.uo_out.value}"

    # Test case 3: A = B (XOR = 0)
    dut.ui_in.value = 0b11111111  # 0xFF
    dut.uio_in.value = 0b11111111  # 0xFF
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00000000, f"Test 3 failed: Expected 00000000, got {dut.uo_out.value}"

    dut._log.info("All test cases passed")
