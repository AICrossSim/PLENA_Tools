"""Memory mapping utilities for generating HBM files.

This module provides functions to convert quantized MXFP data into
memory files compatible with RTL simulation (.mem) or behavioral simulation (.bin).
"""

import os
from pathlib import Path
from typing import List, Union


def _map_block_to_hex(block: List[int], element_width: int) -> str:
    """Convert a block of elements to hex string."""
    if element_width % 4 != 0:
        raise ValueError("element_width must be a multiple of 4")
    hex_digits = element_width // 4
    return ''.join(f"{element:0{hex_digits}X}" for element in block)


def _map_scale_to_hex(scale: int, scale_width: int) -> str:
    """Convert a scale value to hex string."""
    if scale_width % 4 != 0:
        raise ValueError("scale_width must be a multiple of 4")
    hex_digits = scale_width // 4
    return f"{scale:0{hex_digits}X}"


def _hex_to_bytes(hex_str: str) -> bytes:
    """Convert hex string to bytes."""
    hex_str = hex_str.strip()
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    return bytes.fromhex(hex_str)


def generate_hbm(
    blocks: List[List[int]],
    bias: List[int],
    element_width: int,
    bias_width: int,
    directory: Union[str, Path],
    hbm_row_width: int = 256,
    mode: str = "rtl",
) -> Path:
    """Generate HBM memory file from quantized MXFP data.

    Args:
        blocks: List of quantized element blocks, each block is a list of ints
        bias: List of scale/bias values
        element_width: Bit width of each element
        bias_width: Bit width of each scale value
        directory: Output directory path
        hbm_row_width: HBM row width in bits (default: 256)
        mode: "rtl" for .mem hex format, "sim" for .bin binary format

    Returns:
        Path to the generated file
    """
    if mode == "rtl":
        return _generate_hbm_mem(blocks, bias, element_width, bias_width, directory, hbm_row_width)
    elif mode == "sim":
        return _generate_hbm_bin(blocks, bias, element_width, bias_width, directory, hbm_row_width)
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'rtl' or 'sim'.")


def _generate_hbm_mem(
    blocks: List[List[int]],
    bias: List[int],
    element_width: int,
    bias_width: int,
    directory: Union[str, Path],
    hbm_row_width: int,
) -> Path:
    """Generate HBM .mem file (hex text format for RTL simulation).

    Format:
        // HBM_ELEMENTS
        0xDATA_ROW_0
        0xDATA_ROW_1
        ...
        // HBM_SCALES
        0xSCALE_ROW_0
        ...
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    output_file = directory / "hbm.mem"

    # Calculate elements per row
    block_width = element_width * len(blocks[0]) if blocks else element_width
    num_blocks_per_row = hbm_row_width // block_width if block_width > 0 else 1
    num_bias_per_row = hbm_row_width // bias_width if bias_width > 0 else 1

    with open(output_file, "w") as f:
        # Write element section
        f.write("// HBM_ELEMENTS\n")
        row_hex = ""
        count = 0
        for block in blocks:
            row_hex = _map_block_to_hex(block, element_width) + row_hex
            count += 1
            if count >= num_blocks_per_row:
                f.write(f"0x{row_hex}\n")
                row_hex = ""
                count = 0
        if row_hex:
            # Pad remaining row
            padding_bits = (num_blocks_per_row - count) * block_width
            row_hex = "0" * (padding_bits // 4) + row_hex
            f.write(f"0x{row_hex}\n")

        # Write scale section
        f.write("// HBM_SCALES\n")
        row_hex = ""
        count = 0
        for b in bias:
            row_hex = _map_scale_to_hex(b, bias_width) + row_hex
            count += 1
            if count >= num_bias_per_row:
                f.write(f"0x{row_hex}\n")
                row_hex = ""
                count = 0
        if row_hex:
            padding_bits = (num_bias_per_row - count) * bias_width
            row_hex = "0" * (padding_bits // 4) + row_hex
            f.write(f"0x{row_hex}\n")

    return output_file


def _generate_hbm_bin(
    blocks: List[List[int]],
    bias: List[int],
    element_width: int,
    bias_width: int,
    directory: Union[str, Path],
    hbm_row_width: int,
) -> Path:
    """Generate HBM .bin file (binary format for behavioral simulation).

    Format:
        - 8-byte header containing scale data byte offset (little-endian)
        - Element data (packed bytes)
        - Scale data (packed bytes)
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    output_file = directory / "hbm.bin"

    bytes_per_row = hbm_row_width // 8

    # Build element data
    element_data = bytearray()
    row_buffer = bytearray()

    for block in blocks:
        hex_str = _map_block_to_hex(block, element_width)
        block_bytes = _hex_to_bytes(hex_str)
        row_buffer.extend(block_bytes)

        if len(row_buffer) >= bytes_per_row:
            element_data.extend(row_buffer[:bytes_per_row])
            row_buffer = row_buffer[bytes_per_row:]

    if row_buffer:
        padding = bytes_per_row - len(row_buffer)
        row_buffer.extend(b'\x00' * padding)
        element_data.extend(row_buffer)

    # Scale offset = 8 (header) + element data size
    scale_offset = 8 + len(element_data)

    # Build scale data
    scale_data = bytearray()
    row_buffer = bytearray()

    for b in bias:
        hex_str = _map_scale_to_hex(b, bias_width)
        bias_bytes = _hex_to_bytes(hex_str)
        row_buffer.extend(bias_bytes)

        if len(row_buffer) >= bytes_per_row:
            scale_data.extend(row_buffer[:bytes_per_row])
            row_buffer = row_buffer[bytes_per_row:]

    if row_buffer:
        padding = bytes_per_row - len(row_buffer)
        row_buffer.extend(b'\x00' * padding)
        scale_data.extend(row_buffer)

    # Write binary file
    with open(output_file, 'wb') as f:
        header = scale_offset.to_bytes(8, byteorder='little')
        f.write(header)
        f.write(element_data)
        f.write(scale_data)

    return output_file
