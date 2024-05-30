from streamlit.components.v1.components import CustomComponent
from typing import List

import streamlit.elements.image as st_image
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from hashlib import md5
from typing import Literal, Union

from . import _component_func

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
    
    match size:
        case "small":
            ui_height = UI_HEIGHT
            ui_width = UI_WIDTH
        case "medium":
            ui_height = int(2 * UI_HEIGHT)
            ui_width = int(1.25 * UI_WIDTH)
        case "large":
            ui_height = int(4 * UI_HEIGHT)
            ui_width = int(1.5 * UI_WIDTH)
        case _:
            ui_height = int(2 * UI_HEIGHT)
            ui_width = int(1.25 * UI_WIDTH)
    
    return ui_height, ui_width

def annotation(
    
    # add "Output Mode" = "px values", **"relative values mode", "yolo", etc.
    # "original pixel value mode", "resized pixel value mode"  ==> on output, give metadata as well. 
    image_path: str = None,
    label_list: list[str] = [],
    default_label_index: int=None,
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
        
    ui_size: Literal["small", "medium", "large"]= "small",
    ui_left_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_bottom_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_right_size: Union[Literal["small", "medium", "large"], int] = None,
    
    ui_bottom_fill_width: bool = False,
    ui_height: int = None,
    
    read_only: bool = False,
    
    key=None,
) -> CustomComponent:
    if (image_path):
        image = Image.open(image_path)
        image.thumbnail(size=(image_width, image_height))
    
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
            
        if multi_select and isinstance(default_label_index, list):
            _default_label_list = [label_list[i] for i in default_label_index]
        else:
            _default_label_list = []
    
    
    if ui_bottom_fill_width:
        _ui_width = "100vw"
        
    if ui_height:
        _ui_height = ui_height
        
    component_value = _component_func(
        image_url=_image_url,
        image_size=_image_size,
        label_list=label_list,
        
        ui_height=_ui_height,
        ui_width=_ui_width,
        
        default_label_idx=default_label_index,
        key=key,
        
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
        label_type="annotation"
    )
    
    # component_value = _component_func(
    #     image_url=image_url,
    #     image_size=image.size,
    #     label_list=label_list,
    #     ui_width=ui_width,
    #     ui_height=RADIO_HEGIHT,
    #     key=image_url,
    #     label_type="detection"
    # )
    return component_value
