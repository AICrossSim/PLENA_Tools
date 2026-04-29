"""Random tensor generators for MXFP and MXINT quantization."""

import torch
import os
import numpy as np

from plena_utils.torch_fp_conversion import pack_fp_to_bin
from plena_utils.debugger import set_excepthook
from plena_utils.logger import set_logging_verbosity, get_logger
from quant.quantizer.hardware_quantizer import _mx_fp_quantize_hardware
from quant.quantizer.hardware_quantizer.mxint import _mx_int_quantize_hardware

logger = get_logger("rand_gen")
set_logging_verbosity("warning")
set_excepthook()


class Random_MXINT_Tensor_Generator:
    def __init__(self, shape, quant_config, directory=None, filename=None):
        """
        Initialize the random tensor generator with a given shape in MXINT.
        If directory and filename are provided, the tensor will be saved to a file.
        """
        self.shape = shape
        self.directory = directory
        self.filename = filename
        self.quant_config = quant_config

    def tensor_gen(self):
        tensor = torch.randn(self.shape)
        if self.directory and self.filename:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            file_path = os.path.join(self.directory, self.filename)
            torch.save(tensor, file_path)
            logger.debug(f"Tensor saved to {file_path}")

    def tensor_load(self):
        if self.directory and self.filename:
            file_path = os.path.join(self.directory, self.filename)
            if os.path.exists(file_path):
                tensor = torch.load(file_path)
                logger.debug(f"Tensor loaded from {file_path}")
                return tensor
            else:
                logger.error(f"File {file_path} does not exist.")
                return None
        else:
            logger.error("Directory and filename must be specified to load the tensor.")
            return None

    def quantize_tensor(self, tensor):
        bm_x, per_block_exponent, per_block_mantissa, per_block_scaling = _mx_int_quantize_hardware(
            tensor,
            width=self.quant_config["man_width"],
            exponent_width=self.quant_config["exp_width"],
            block_size=self.quant_config["block_size"],
            skip_first_dim=self.quant_config["skip_first_dim"],
        )

        block_list = []
        scaling_list = []

        for i in range(per_block_mantissa.shape[0]):
            block_list.append(per_block_mantissa[i] * 2 ** (self.quant_config["man_width"] - 1).tolist())
            scaling_list.append(int(per_block_scaling[i]))

        return block_list, scaling_list


class Random_MXFP_Tensor_Generator:
    def __init__(self, shape, quant_config, config_settings=None, directory=None, filename=None):
        """
        Initialize the random tensor generator with a given shape in MXFP.
        If directory and filename are provided, the tensor will be saved to a file.
        """
        self.shape = shape
        self.directory = directory
        self.filename = filename
        self.quant_config = quant_config
        self.config_settings = config_settings or {}

    def tensor_gen(self):
        tensor = torch.randn(self.shape)
        if self.directory and self.filename:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            file_path = os.path.join(self.directory, self.filename)
            torch.save(tensor, file_path)
            logger.debug(f"Tensor saved to {file_path}")

    def tensor_load(self):
        if self.directory and self.filename:
            file_path = os.path.join(self.directory, self.filename)
            if os.path.exists(file_path):
                tensor = torch.load(file_path)
                logger.debug(f"Tensor loaded from {file_path}")
                return tensor
            else:
                logger.error(f"File {file_path} does not exist.")
                return None
        else:
            logger.error("Directory and filename must be specified to load the tensor.")
            return None

    def quantize_tensor(self, tensor):
        """
        Quantize tensor to MXFP format.
        Returns (block_list, scaling_list).
        """
        if tensor.ndim == 1:
            tensor = tensor.unsqueeze(0)

        bm_x, per_block_exponent, per_block_mantissa, per_block_scaling = _mx_fp_quantize_hardware(
            tensor,
            width=self.quant_config["exp_width"] + self.quant_config["man_width"] + 1,
            exponent_width=self.quant_config["exp_width"],
            exponent_bias_width=self.quant_config["exp_bias_width"],
            block_size=self.quant_config["block_size"],
            skip_first_dim=self.quant_config["skip_first_dim"],
        )

        block_list = []
        scaling_list = []

        for i in range(per_block_mantissa.shape[0]):
            bin_block = pack_fp_to_bin(
                per_block_exponent[i],
                per_block_mantissa[i],
                self.quant_config["exp_width"],
                self.quant_config["man_width"],
            )
            block_list.append(bin_block.tolist())
            scaling_list.append(int(per_block_scaling[i]))

        return block_list, scaling_list
