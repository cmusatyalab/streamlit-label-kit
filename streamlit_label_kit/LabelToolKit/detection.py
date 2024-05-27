import os
import streamlit.components.v1 as components
from streamlit.components.v1.components import CustomComponent
from typing import List

import streamlit as st
import streamlit.elements.image as st_image
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from hashlib import md5
from typing import Literal, Union

from .__init__ import _component_func

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
UI_WIDTH = 198

#'''
# bboxes:
# [[x,y,w,h],[x,y,w,h]]
# labels:
# [0,3]
#'''


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


def detection(
    image_path,
    label_list,
    bboxes=None,
    labels=[],
    metaDatas: list[list[str]] = [],
    
    height=512,
    width=512,
    
    line_width=1.0,
    
    ui_position: Literal["right", "left"] = "right",
    class_select_position: Literal["right", "left", "bottom"] = None,
    item_editor_position: Literal["right", "left"] = None,
    item_selector_position: Literal["right", "left"] = None,

    class_select_type: Literal["select", "radio"] = "select",
    item_editor: bool = True,
    item_selector: bool = True,
    edit_description: bool = False,
    
    ui_size: Literal["small", "medium", "large"]= "small",
    ui_left_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_bottom_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_right_size: Union[Literal["small", "medium", "large"], int] = None,
    
    key=None,
) -> CustomComponent:
    image = Image.open(image_path)
    original_image_size = image.size
    image.thumbnail(size=(width, height))
    
    resized_image_size = image.size
    scale = original_image_size[0] / resized_image_size[0]
    
    _class_select_pos = class_select_position or ui_position
    _item_editor_pos = item_editor_position or ui_position
    _item_selector_pos = item_selector_position or ui_position
    _edit_meta = not edit_description
    
    _, _left_size = _calc_size(ui_left_size or ui_size)
    _bottom_size, _ = _calc_size(ui_bottom_size or ui_size)
    _, _right_size = _calc_size(ui_right_size or ui_size)
    
    _select_type = "radio" if class_select_type != "select" else "select"
    
    image_url = st_image.image_to_url(
        image,
        image.size[0],
        True,
        "RGB",
        "PNG",
        f"annotation-{md5(image.tobytes()).hexdigest()}-{key}",
    )
    if image_url.startswith("/"):
        image_url = image_url[1:]
        
    color_map = get_colormap(label_list, colormap_name="gist_rainbow")
    
    num_bboxes = len(bboxes)

    if len(labels) > num_bboxes:
        labels = labels[:num_bboxes]
    else:
        labels.extend(["0"] * (num_bboxes - len(labels)))

    if len(metaDatas) > num_bboxes:
        metaDatas = metaDatas[:num_bboxes]
    else:
        metaDatas.extend([[]] * (num_bboxes - len(metaDatas)))
    
    bbox_info = [
        {
            "bbox": [b / scale for b in item[0]],
            "label_id": item[1],
            "label": label_list[item[1]],
            "meta": item[2]
        }
        for item in zip(bboxes, labels, metaDatas)
    ]
    
    # ui_height = RADIO_HEGIHT
    # ui_width = UI_WIDTH
    # match ui_size:
    #     case "small":
    #         ui_height = ui_height
    #         ui_width = ui_width
    #     case "middle":
    #         ui_height = int(2 * ui_height)
    #         ui_width = int(1.25 * ui_width)
    #     case "large":
    #         ui_height = int(4 * ui_height)
    #         ui_width = int(1.5 * ui_width)
    
    component_value = _component_func(
        image_url=image_url,
        image_size=image.size,
        label_list=label_list,
        bbox_info=bbox_info,
        color_map=color_map,
        line_width=line_width,
        ui_width=20,
        ui_height=20,
        
        edit_meta=_edit_meta,
        edit_description=True,
        
        class_select_type=_select_type,
        item_editor=item_editor,
        item_selector=item_selector,

        class_select_position=_class_select_pos,
        item_editor_position=_item_editor_pos,
        item_selector_position=_item_selector_pos,
        
        ui_left_size=_left_size,
        ui_bottom_size=_bottom_size,
        ui_right_size=_right_size,
        
        key=key,
        label_type="detection"
    )
    bbox = None
    if component_value is not None:
        return component_value
        bbox = component_value["bbox"]
        
        bbox = [
            {
                "bbox": [b * scale for b in item["bbox"]],
                "label_id": item["label_id"],
                "label": item["label"],
                "meta": item["meta"],
            }
            for item in bbox
        ]
    return bbox