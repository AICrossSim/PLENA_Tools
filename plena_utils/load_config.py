import re

import toml


def load_svh_settings(file_path):
    """
    Parse SystemVerilog `parameter` definitions in an .svh/.sv file
    """
    param_pattern = re.compile(r"\s*(?:localparam|parameter)\s+(\w+)\s*=\s*([^;]+);")
    hardware_settings = {}

    with open(file_path) as f:
        for line in f:
            match = param_pattern.match(line)
            if match:
                name, value_str = match.groups()
                value_str = value_str.strip()
                # Try integer conversion first
                try:
                    value = int(value_str)
                except ValueError:
                    # Fallback to raw string (could be expression or real number)
                    continue
                hardware_settings[name] = value
    return hardware_settings


def load_json(file_path):
    """
    Load machine learning model configuration from a JSON file.
    """
    import json

    with open(file_path) as f:
        ml_config = json.load(f)
    return ml_config


def load_toml_config(file_path, section_to_load=None, mode="BEHAVIOR"):
    """
    Load configuration from TOML file.

    Args:
        file_path: Path to the TOML file
        section_to_load: Section name (CONFIG, PRECISION, LATENCY)
        mode: Top-level mode section (BEHAVIOR or ANALYTIC)

    Returns:
        dict: The requested configuration section
    """
    with open(file_path) as f:
        full_toml = toml.load(f)

    # Get the mode section (BEHAVIOR or ANALYTIC)
    mode_section = full_toml.get(mode, {})
    return mode_section.get(section_to_load, {})


def load_precision_from_svh(definitions_path):
    """
    Load precision settings from hardware SVH files.

    Args:
        definitions_path: Path to the definitions directory containing
                         precision.svh and configuration.svh

    Returns:
        tuple: (precision_settings, config_settings)
            precision_settings: dict with block_size, exp_width, man_width,
                              scale_exp_width, int_width
            config_settings: dict with raw config from configuration.svh
    """
    from pathlib import Path
    definitions_path = Path(definitions_path)

    precision_svh = definitions_path / "precision.svh"
    config_svh = definitions_path / "configuration.svh"

    precision = load_svh_settings(str(precision_svh))
    config = load_svh_settings(str(config_svh))

    precision_settings = {
        "block_size": precision.get("BLOCK_DIM", 8),
        "exp_width": precision.get("ACT_MXFP_EXP_WIDTH", 4),
        "man_width": precision.get("ACT_MXFP_MANT_WIDTH", 3),
        "scale_exp_width": precision.get("MX_SCALE_WIDTH", 8),
        "int_width": precision.get("INT_DATA_WIDTH", 32),
    }

    return precision_settings, config
