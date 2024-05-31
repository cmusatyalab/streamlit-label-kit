#
# Streamlit components for general labeling tasks
#
# Copyright (c) 2024 Carnegie Mellon University
# SPDX-License-Identifier: GPL-2.0-only
#

from pathlib import Path

import streamlit.components.v1 as components

build_path = Path(__file__).resolve().parent.joinpath("frontend", "build")
_component_func = components.declare_component("st-label-kit", path=str(build_path))
