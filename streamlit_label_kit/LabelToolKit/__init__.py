import os
import streamlit.components.v1 as components
from typing import List

import numpy as np
import matplotlib.pyplot as plt
from streamlit_label_kit import IS_RELEASE

if IS_RELEASE:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(absolute_path, "frontend/build")
    _component_func = components.declare_component("st-label-kit", path=build_path)
else:
    _component_func = components.declare_component(
        "st-label-kit", url="http://localhost:3000"
    )