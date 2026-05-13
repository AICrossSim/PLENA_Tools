"""PLENA Verification Tools.

Shared verification utilities for RTL and behavioral simulation.
Provides memory comparison, viewing, and test environment creation.
"""

from verification.check_mem import (
    compare_fpsram_with_golden,
    compare_hbm_with_golden,
    compare_vram_with_golden,
    parse_golden_output,
    print_comparison_results,
    read_bin_file_as_array,
    read_fpsram_bin_file_as_array,
    read_hbm_bin_file_as_array,
    reorder_stride_mode,
    slice_rows,
)
from verification.create_sim_env import create_sim_env, np_array_to_str_2f
from verification.test_data_gen import generate_and_save_random_weights, get_weights_path
from verification.view_mem import (
    view_bin_file_by_row_fp,
    view_bin_file_by_row_int,
    view_fpsram_bin_file,
)
from verification.verify_rtl_sim import (
    parse_hbm_result_file,
    verify_hbm,
    verify_vram,
    compare_results,
    mx_to_float,
    mxint_to_float,
    save_vector_result_as_fp,
)
from verification.view_vector_result import (
    view_vector_result_as_fp,
    view_vector_result_as_hex,
    view_vector_result_as_binary,
    parse_vector_result_file,
)
from verification.hbm_interpreter import (
    read_hbm_mem_file,
    interpret_hbm_to_float,
    compare_with_original,
    dump_hbm_raw,
)
from verification.verify_mxint_encoding import (
    verify_mxint_encoding,
    read_hbm_mxint,
    mxint_to_float,
)

__all__ = [
    # check_mem
    "compare_fpsram_with_golden",
    "compare_hbm_with_golden",
    "compare_vram_with_golden",
    "parse_golden_output",
    "print_comparison_results",
    "read_bin_file_as_array",
    "read_fpsram_bin_file_as_array",
    "read_hbm_bin_file_as_array",
    "reorder_stride_mode",
    "slice_rows",
    # create_sim_env
    "create_sim_env",
    "np_array_to_str_2f",
    # test_data_gen
    "generate_and_save_random_weights",
    "get_weights_path",
    # view_mem
    "view_bin_file_by_row_fp",
    "view_bin_file_by_row_int",
    "view_fpsram_bin_file",
    # verify_rtl_sim
    "parse_hbm_result_file",
    "verify_hbm",
    "verify_vram",
    "compare_results",
    "mx_to_float",
    "mxint_to_float",
    "save_vector_result_as_fp",
    # view_vector_result
    "view_vector_result_as_fp",
    "view_vector_result_as_hex",
    "view_vector_result_as_binary",
    "parse_vector_result_file",
    # hbm_interpreter
    "read_hbm_mem_file",
    "interpret_hbm_to_float",
    "compare_with_original",
    "dump_hbm_raw",
    # verify_mxint_encoding
    "verify_mxint_encoding",
    "read_hbm_mxint",
    "mxint_to_float",
]
