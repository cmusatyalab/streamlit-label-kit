#
# Streamlit components for general labeling tasks
#
# Copyright (c) 2024 Carnegie Mellon University
# SPDX-License-Identifier: GPL-2.0-only
#

from __future__ import annotations
from hashlib import md5
from typing import Literal, Union, List
import matplotlib.pyplot as plt
import numpy as np
import streamlit.elements.image as st_image
from PIL import Image
from streamlit.components.v1.components import CustomComponent
from . import _component_func, thumbnail_with_upscale


def get_colormap(label_names, colormap_name="gist_rainbow"):
    colormap = {}
    cmap = plt.get_cmap(colormap_name)
    for idx, l in enumerate(label_names):
        rgb = [int(d) for d in np.array(cmap(float(idx) / len(label_names))) * 255][:3]
        colormap[l] = "#%02x%02x%02x" % tuple(rgb)
    return colormap

SELECT_HEIGHT = 60
RADIO_HEGIHT = 34
UI_HEIGHT = 34
UI_WIDTH = 168

def _calc_size(size) :
    if isinstance(size, (int, float)):
        return size, size
            
    if size == "small":
        ui_height = UI_HEIGHT
        ui_width = UI_WIDTH
    elif size == "medium":
        ui_height = int(2 * UI_HEIGHT)
        ui_width = int(1.25 * UI_WIDTH)
    elif size == "large":
        ui_height = int(4 * UI_HEIGHT)
        ui_width = int(1.5 * UI_WIDTH)
    else:
        ui_height = int(2 * UI_HEIGHT)
        ui_width = int(1.25 * UI_WIDTH)
    
    return ui_height, ui_width

def annotation(
    image_path: str = None,
    label_list: List[str] = [],
    label_index: Union[int, List[int]]=None,
    image_height: int=512,
    image_width: int=512,
    classification: bool = False,
    multi_select: bool = False,
    ui_position: Literal["right", "left"] = "right",
    class_select_position: Literal["right", "left", "bottom"] = None,
    meta_editor_position: Literal["right", "left"] = None,
    class_select_type: Literal["select", "radio"] = "radio",
    meta_editor: bool = False,
    edit_description: bool = False,
    meta_data: List[str] = [],
    ui_size: Literal["small", "medium", "large"]= "small",
    ui_left_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_bottom_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_right_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_bottom_fill_width: bool = False,
    ui_height: int = None,
    read_only: bool = False,
    component_alignment: Literal["left", "center", "right"] = "left",
    key=None,
) -> CustomComponent:
    """
    Provides a user interface for annotating images, enabling the interactive assignment of labels/classes
    or editing of metadata/descriptions. This function can also be used to display only the UI components without
    an image by omitting the `image_path` parameter.

    Args:
        image_path (str, optional): Path to the image file. If not provided, no image is displayed.
        label_list (list[str], optional): List of available labels for classification.
        label_index (Union[int, list[int]], optional): Index or indices of the initially selected label(s) from `label_list`.
        image_height (int, optional): The height to which the image should be resized.
        image_width (int, optional): The width to which the image should be resized.
        classification (bool, optional): If True, enables the classification UI. Defaults to False.
        multi_select (bool, optional): Allows selection of multiple labels if True.
        ui_position (Literal["right", "left"], optional): Default position for UI controls.
        class_select_position (Literal["right", "left", "bottom"], optional): Position of the class selector UI.
        meta_editor_position (Literal["right", "left"], optional): Position of the metadata editor UI.
        class_select_type (Literal["select", "radio"], optional): Type of UI control for class selection.
        meta_editor (bool, optional): If True, enables metadata editing UI.
        edit_description (bool, optional): If True, enables an additional description field for metadata.
        meta_data (list[str], optional): List of metadata strings associated with the image.
        ui_size (Literal["small", "medium", "large"], optional): Base size for UI components.
        ui_left_size (Union[Literal, int], optional): Custom size for left-positioned UI elements.
        ui_bottom_size (Union[Literal, int], optional): Custom size for bottom-positioned UI elements.
        ui_right_size (Union[Literal, int], optional): Custom size for right-positioned UI elements.
        ui_bottom_fill_width (bool, optional): If True, the bottom UI fills the width of the viewport.
        ui_height (int, optional): Custom height for the UI components.
        read_only (bool, optional): If True, disables any interactions, making the UI read-only.
        component_alignment (Literal["left", "center", "right"], optional): Alignment of the UI components.
        key (any, optional): A unique key to differentiate this instance when using multiple components.

    Returns:
        CustomComponent: A Streamlit CustomComponent that renders the UI for image annotation.

    Output Format:
        {
            'label': str,   # Name of the selected label.
            'meta': [str],  # List of metadata strings associated with the annotation.
            'key': key,     # Unique identifier for the returned value.
        }
    """


    #WARNNING: If you are "inputing" data to "annotation", always provide appropriate value to the "meta_data" argument
    
    if (image_path):
        image = Image.open(image_path)
        image = thumbnail_with_upscale(image, (image_width, image_height))
    
    if (not classification and not meta_editor):
        return None
    
    _class_select_pos = class_select_position or ui_position
    _meta_editor_pos = meta_editor_position or ui_position
    _edit_meta = not edit_description and meta_editor
    
    _ui_height, _ui_width = _calc_size(ui_size)
    _, _left_size = _calc_size(ui_left_size or ui_size)
    _bottom_size, _ = _calc_size(ui_bottom_size or ui_size)
    _, _right_size = _calc_size(ui_right_size or ui_size)

    _select_type = "radio" if class_select_type != "select" else "select"

    if image_path == None:
        _image_url = ""
        _default_label_list = []
        _image_size = [0,0]

    else:
        _image_url = st_image.image_to_url(
            image,
            image.size[0],
            True,
            "RGB",
            "PNG",
            f"annotation-{md5(image.tobytes()).hexdigest()}-{key}",
        )
        _image_size = image.size
        if _image_url.startswith("/"):
            _image_url = _image_url[1:]
            
        if multi_select and isinstance(label_index, list):
            _default_label_list = [label_list[i] for i in label_index]
        else:
            _default_label_list = []
    
    
    if ui_bottom_fill_width:
        _ui_width = "100vw"
        
    if ui_height:
        _ui_height = ui_height
        
    _justify_content = {"left": "start", "center":"center", "right":"end"}[component_alignment]
        
    
    component_value = _component_func(
        image_url=_image_url,
        image_size=_image_size,
        label_list=label_list,
        ui_height=_ui_height,
        ui_width=_ui_width,
        default_label_idx=label_index,
        key=key,
        meta_info=meta_data,
        multi_select=multi_select,
        
        edit_class=classification,
        edit_meta=_edit_meta,
        edit_description=meta_editor and edit_description,
        
        class_select_type=_select_type,
        meta_editor=meta_editor,
        
        class_select_position=_class_select_pos,
        meta_editor_position=_meta_editor_pos,
        
        ui_left_size=_left_size,
        ui_bottom_size=_bottom_size,
        ui_right_size=_right_size,
        
        read_only=read_only,
        
        default_multi_label_list=_default_label_list,
        justify_content=_justify_content,
        label_type="annotation"
    )
    
    key = 0
    label = []
    meta = []
    if component_value:
        label = component_value["label"]
        key = int(component_value["key"])
        meta = component_value["meta"]
    result = {"label": label, "meta": meta, "key": key}
        
    
    return result
