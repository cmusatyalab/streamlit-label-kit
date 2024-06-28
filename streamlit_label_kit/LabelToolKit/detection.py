#
# Streamlit components for general labeling tasks
#
# Copyright (c) 2024 Carnegie Mellon University
# SPDX-License-Identifier: GPL-2.0-only
#

from __future__ import annotations
from hashlib import md5
from typing import Literal, Union, List, Dict
import matplotlib.pyplot as plt
import numpy as np
import streamlit.elements.image as st_image
from PIL import Image
from streamlit.components.v1.components import CustomComponent
from . import _component_func, convert_bbox_format, relative_to_absolute, absolute_to_relative, thumbnail_with_upscale


def _get_colormap(label_names, colormap_name="gist_rainbow"):
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

def _calc_size(size):
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

def detection(
    #read_only
    image_path,
    label_list,
    bboxes=None,
    bbox_ids=[],
    labels=[],
    read_only=False,
    info_dict: List[Dict[str:str]] = [],
    meta_data: List[List[str]] = [],
    bbox_format: Literal["XYWH", "XYXY", "CXYWH", "REL_XYWH", "REL_XYXY", "REL_CXYWH"] = "XYWH",
    image_height=512,
    image_width=512,
    line_width=1.0,
    ui_position: Literal["right", "left"] = "left",
    class_select_position: Literal["right", "left", "bottom"] = None,
    item_editor_position: Literal["right", "left"] = None,
    item_selector_position: Literal["right", "left"] = None,
    class_select_type: Literal["select", "radio"] = "select",
    item_editor: bool = False,
    item_selector: bool = False,
    edit_meta: bool = False,
    edit_description: bool = False,
    ui_size: Literal["small", "medium", "large"] = "small",
    ui_left_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_bottom_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_right_size: Union[Literal["small", "medium", "large"], int] = None,
    bbox_show_label: bool = False,
    bbox_show_info: bool = False,
    component_alignment: Literal["left", "center", "right"] = "left",
    key=None,
) -> CustomComponent:
    """
    Configures and renders a UI component for annotating images with bounding boxes and labels,
    optionally allowing the user to edit metadata and other details.

    Args:
        image_path (str): Path to the image file for annotation.
        label_list (List[str]): List of labels for bounding boxes.
        bboxes (List[Tuple[float, float, float, float]], optional): List of bounding boxes in the format specified by `bbox_format`.
        bbox_ids (List[str], optional): Unique identifiers for each bounding box.
        labels (List[int], optional): Indices from `label_list` corresponding to each bounding box.
        read_only (bool, optional): Disables editing features, making UI read-only.
        info_dict (List[Dict[str, str]], optional): List of dictionaries with additional info for each bounding box.
        meta_data (List[List[str]], optional): Metadata for each bounding box.
        bbox_format (Literal["XYWH", "XYXY", "CXYWH", "REL_XYWH", "REL_XYXY", "REL_CXYWH"], optional): Format of the bounding boxes provided.
        image_height (int, optional): Height to which the input image is resized.
        image_width (int, optional): Width to which the input image is resized.
        line_width (float, optional): Line width used for drawing bounding boxes.
        ui_position (Literal["right", "left"], optional): Default position for non-specific UI components.
        class_select_position (Literal["right", "left", "bottom"], optional): Position of the class selection UI component.
        item_editor_position (Literal["right", "left"], optional): Position of the item editor UI component.
        item_selector_position (Literal["right", "left"], optional): Position of the item selector UI component.
        class_select_type (Literal["select", "radio"], optional): Type of UI control for class selection.
        item_editor (bool, optional): Enables the item editor component.
        item_selector (bool, optional): Enables the item selector component.
        edit_meta (bool, optional): Allows editing of metadata.
        edit_description (bool, optional): Enables description field for metadata editing.
        ui_size (Literal["small", "medium", "large"], optional): Base size for UI components.
        ui_left_size (Union[Literal, int], optional): Specific size for UI components on the left.
        ui_bottom_size (Union[Literal, int], optional): Specific size for UI components at the bottom.
        ui_right_size (Union[Literal, int], optional): Specific size for UI components on the right.
        bbox_show_label (bool, optional): If True, display labels near bounding boxes.
        bbox_show_info (bool, optional): If True, display additional info near bounding boxes.
        component_alignment (Literal["left", "center", "right"], optional): Alignment of the component within its container.
        key (any, optional): A unique key to differentiate this instance when using multiple instances.

    Returns:
        CustomComponent: A Streamlit CustomComponent that renders the detection interface.

    Output Format:
        - For regular usage:
            {
                "bbox": [
                    {
                        "bboxes": [list],   # Bbox coordinates in the specified format
                        "labels": int,      # Label index for the bbox
                        "label_names": str, # Label name for the bbox
                        "meta_data": [str], # List of metadata strings
                        "info_dict": {str: str}, # Dictionary of additional string-string pairs
                        "bbox_ids": str,    # Unique identifier for the bbox
                    }
                ],
                "image_size": (int, int), # Original dimensions of the input image
                "bbox_format": str,      # Format of the bounding box data
                "key": str               # Unique identifier for the returned value
            }
    """

    # Load Image and convert size
    image = Image.open(image_path)
    original_image_size = image.size
    image = thumbnail_with_upscale(image, (image_width, image_height))

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

    color_map = _get_colormap(label_list, colormap_name="gist_rainbow")

    resized_image_size = image.size
    scale = original_image_size[0] / resized_image_size[0]

    # Configure UI position and size
    _class_select_pos = class_select_position or ui_position
    _item_editor_pos = item_editor_position or ui_position
    _item_selector_pos = item_selector_position or ui_position
    _edit_meta = edit_meta
    _edit_description = not edit_meta and edit_description

    _, _left_size = _calc_size(ui_left_size or ui_size)
    _bottom_size, _ = _calc_size(ui_bottom_size or ui_size)
    _, _right_size = _calc_size(ui_right_size or ui_size)

    _select_type = "radio" if class_select_type != "select" else "select"

    # Configure default labels, meta_data, additional_info
    num_bboxes = len(bboxes)
    if len(labels) > num_bboxes:
        labels = labels[:num_bboxes]
    else:
        labels.extend(["0"] * (num_bboxes - len(labels)))

    if len(meta_data) > num_bboxes:
        meta_data = meta_data[:num_bboxes]
    else:
        meta_data.extend([[]] * (num_bboxes - len(meta_data)))
        
    if len(info_dict) > num_bboxes:
        info_dict = info_dict[:num_bboxes]
    else:
        info_dict.extend([dict()] * (num_bboxes - len(info_dict)))
        
    if len(bbox_ids) > num_bboxes:
        bbox_ids = bbox_ids[:num_bboxes]
    else:
        bbox_ids.extend(["bbox-" + str(i + len(bbox_ids)) for i in range(num_bboxes - len(bbox_ids))])

    # Convert BBOX Format to XYWH
    if "REL" in bbox_format:
        bboxes = [
            relative_to_absolute(bbox, original_image_size[0], original_image_size[1])
            for bbox in bboxes
        ]
        original_format = bbox_format.replace("REL_", "")
    else:
        original_format = bbox_format
    bboxes = [convert_bbox_format(bbox, original_format, "XYWH") for bbox in bboxes]

    bbox_info = [
        {
            "bbox": [b / scale for b in item[0]],
            "label": label_list[item[1]],
            "meta": item[2],
            "additional_data": item[3],
            "id": item[4],
        }
        for item in zip(bboxes, labels, meta_data, info_dict, bbox_ids)
    ]
    
    _justify_content = {"left": "start", "center":"center", "right":"end"}[component_alignment]

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
        edit_description=_edit_description,
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
        read_only=read_only,
        bbox_show_label=bbox_show_label,
        bbox_show_additional=bbox_show_info,
        justify_content=_justify_content,
        label_type="detection",
    )
    
    _bboxes = []
    key = 0
    if component_value is not None:
        bboxes = component_value["bbox"]
        key = int(component_value["key"])
        _bboxes = [
            {
                "bboxes": [b * scale for b in item["bbox"]],
                "bbox_ids" : item["id"],
                "labels": item["label_id"],
                "label_names": item["label"],
                "meta_data": item["meta"],
                "info_dict": item["additional_data"],
            }
            for item in bboxes
        ]

        # Convert back to original format
        if "REL" in bbox_format:
            bboxes = [
                convert_bbox_format(bbox["bboxes"], "XYWH", original_format)
                for bbox in _bboxes
            ]
            bboxes = [
                absolute_to_relative(bbox, original_image_size[0], original_image_size[1])
                for bbox in bboxes
            ]
        else:
            bboxes = [
                convert_bbox_format(bbox["bboxes"], "XYWH", original_format)
                for bbox in _bboxes
            ]
        for i in range(len(_bboxes)):
            _bboxes[i]["bboxes"] = bboxes[i]
            
            
    return {
        "bbox": _bboxes,
        "image_size": original_image_size,
        "resized_image_size": resized_image_size,
        "bbox_format": bbox_format,
        "key": key,
    }
