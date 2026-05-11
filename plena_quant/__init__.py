"""
plena_quant - Quantization utilities for MXFP and MXINT formats.

This package provides hardware-accurate quantization functions for:
- MXFP (Microscaling Floating Point): Block floating point with shared exponent bias
- MXINT (Microscaling Integer): Block floating point with shared exponent

Usage:
    from plena_quant.mxfp import _mx_fp_quantize_hardware, Random_MXFP_Tensor_Generator
    from plena_quant.mxint import _mx_int_quantize_hardware, Random_MXINT_Tensor_Generator
    from plena_quant.common import _minifloat_ieee_quantize_hardware

For backward compatibility with old import paths:
    from plena_quant.quantizer.hardware_quantizer import _minifloat_ieee_quantize_hardware
    from plena_quant.quantizer.hardware_quantizer.mxfp import _mx_fp_quantize_hardware
    from plena_quant.quantizer import minifloat_ieee_quantizer
"""

# Common utilities
from .common import (
    _minifloat_ieee_quantize_hardware,
    _minifloat_denorm_quantize_hardware,
    block,
    unblock,
    my_clamp,
    my_round,
    my_floor,
    hardware_round,
    fixed_point_cast,
)

# MXFP module
from .mxfp import (
    _mx_fp_quantize_hardware,
    pack_fp_to_bin,
    bin_2_fp,
    fp_2_bin,
    Random_MXFP_Tensor_Generator,
)

# MXINT module
from .mxint import (
    _mx_int_quantize_hardware,
    Random_MXINT_Tensor_Generator,
)

# Quantizer submodule (for backward compatibility)
from .quantizer import (
    minifloat_ieee_quantizer,
    mx_int_quantizer,
    mxfp_quantizer,
    fixed_point_quantizer,
    fixed_point_floor_quantizer,
)
