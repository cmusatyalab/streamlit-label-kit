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

from . import _component_func


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

#'''
# bboxes:
# [[x,y,w,h],[x,y,w,h]]
# labels:
# [0,3]
#'''


def convert_bbox_format(
    bbox: tuple[float, float, float, float],
    input_format: Literal["XYWH", "XYXY", "CXYWH"],
    output_format: Literal["XYWH", "XYXY", "CXYWH"],
) -> tuple[float, float, float, float]:
    """
    Convert bounding box between specified formats.

    Args:
    bbox (Tuple[float, float, float, float]): The bounding box coordinates.
    input_format (str): The format of the input bounding box.
    output_format (str): The format to convert the bounding box to.

    Returns:
    Tuple[float, float, float, float]: The bounding box in the new format.
    """
    if input_format == output_format:
        return bbox

    x, y, w, h = 0, 0, 0, 0

    # Unpack the bounding box based on the input format
    if input_format == "XYXY":
        x1, y1, x2, y2 = bbox
        x, y, w, h = x1, y1, x2 - x1, y2 - y1
    elif input_format == "XYWH":
        x, y, w, h = bbox
    elif input_format == "CXYWH":
        cx, cy, w, h = bbox
        x, y = cx - w / 2, cy - h / 2

    # Convert to the output format
    if output_format == "XYXY":
        x1, y1, x2, y2 = x, y, x + w, y + h
        return (x1, y1, x2, y2)
    elif output_format == "XYWH":
        return (x, y, w, h)
    elif output_format == "CXYWH":
        cx, cy = x + w / 2, y + h / 2
        return (cx, cy, w, h)


def relative_to_absolute(
    bbox: tuple[float, float, float, float], image_width: int, image_height: int
) -> tuple[float, float, float, float]:
    """
    Convert relative bbox coordinates to absolute pixel coordinates.

    Args:
    bbox (Tuple[float, float, float, float]): The bounding box in relative format.
    image_width (int): The width of the image in pixels.
    image_height (int): The height of the image in pixels.

    Returns:
    Tuple[float, float, float, float]: The bounding box in absolute pixel coordinates.
    """
    rx1, ry1, rx2, ry2 = bbox  # Assuming bbox in format REL_XYXY
    ax1, ay1 = rx1 * image_width, ry1 * image_height
    ax2, ay2 = rx2 * image_width, ry2 * image_height
    return (ax1, ay1, ax2, ay2)


def absolute_to_relative(
    bbox: tuple[float, float, float, float], image_width: int, image_height: int
) -> tuple[float, float, float, float]:
    """
    Convert absolute pixel bbox coordinates to relative coordinates.

    Args:
    bbox (Tuple[float, float, float, float]): The bounding box in absolute pixel format.
    image_width (int): The width of the image in pixels.
    image_height (int): The height of the image in pixels.

    Returns:
    Tuple[float, float, float, float]: The bounding box in relative coordinates.
    """
    ax1, ay1, ax2, ay2 = bbox  # Assuming bbox in format XYXY
    rx1, ry1 = ax1 / image_width, ay1 / image_height
    rx2, ry2 = ax2 / image_width, ay2 / image_height
    return (rx1, ry1, rx2, ry2)


def _calc_size(size):
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


def segmentation(
    image_path,
    label_list,
    masks=None,
    mask_ids=[],
    labels=[],
    read_only=False,
    info_dict: list[dict[str:str]] = [],
    meta_data: list[list[str]] = [],
    bbox_format: Literal["XYWH", "XYXY", "CXYWH", "REL_XYWH", "REL_XYXY", "REL_CXYWH"] = "XYWH",
    image_height=512,
    image_width=512,
    line_width=1.0,
    ui_position: Literal["right", "left"] = "left",
    class_select_position: Literal["right", "left", "bottom"] = None,
    item_editor_position: Literal["right", "left"] = None,
    item_selector_position: Literal["right", "left"] = None,
    item_editor: bool = False,
    item_selector: bool = False,
    edit_meta: bool = False,
    edit_description: bool = False,
    ui_size: Literal["small", "medium", "large"] = "small",
    ui_left_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_bottom_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_right_size: Union[Literal["small", "medium", "large"], int] = None,
    auto_segmentation: bool = False,
    component_alignment: Literal["left", "center", "right"] = "left",
    key=None,
) -> CustomComponent:
    """
    Process an image for segmentation, providing a UI for interaction, and enabling editing and mask generation.

    Args:
        image_path (str): File path of the image to be segmented.
        label_list (List[str]): Labels used for classifying segmentation masks.
        masks (List[np.ndarray], optional): Initial list of mask arrays corresponding to each label.
        mask_ids (List[str], optional): Unique identifiers for each mask.
        labels (List[int], optional): Indices from `label_list` corresponding to each mask.
        read_only (bool, optional): If True, disable any modifications to masks and metadata.
        info_dict (List[dict], optional): List of dictionaries with additional information for each mask.
        meta_data (List[List[str]], optional): Metadata associated with each mask, provided as a list of strings.
        bbox_format (Literal["XYWH", "XYXY", "CXYWH", "REL_XYWH", "REL_XYXY", "REL_CXYWH"], optional): Format of bounding box data provided (for auto_segmentation output)
        image_height (int, optional): The height to which the image is resized.
        image_width (int, optional): The width to which the image is resized.
        line_width (float, optional): Width of the lines used to draw bounding boxes.
        ui_position (Literal["right", "left"], optional): Default position for UI controls.
        class_select_position (Literal["right", "left", "bottom"], optional): Position of the class selector UI.
        item_editor_position (Literal["right", "left"], optional): Position of the item editor UI.
        item_selector_position (Literal["right", "left"], optional): Position of the item selector UI.
        item_editor (bool, optional): Enable the item editor for modifying masks.
        item_selector (bool, optional): Enable the item selector for selecting different masks.
        edit_meta (bool, optional): Allow editing of mask metadata.
        edit_description (bool, optional): Enable a description field for additional mask information.
        ui_size (Literal["small", "medium", "large"], optional): Base size for UI components.
        ui_left_size (Union[Literal["small", "medium", "large"], int], optional): Custom size for left-positioned UI elements.
        ui_bottom_size (Union[Literal["small", "medium", "large"], int], optional): Custom size for bottom-positioned UI elements.
        ui_right_size (Union[Literal["small", "medium", "large"], int], optional): Custom size for right-positioned UI elements.
        auto_segmentation (bool, optional): For "new" segmentation, user provides bounding boxes, instead of full masks.
        component_alignment (Literal["left", "center", "right"], optional): Alignment of the UI components within the interface.
        key (any, optional): A unique key to identify the Streamlit component instance.

    Returns:
        CustomComponent: A Streamlit CustomComponent that renders the interactive segmentation interface.

    Output Format:
        - For regular usage:
            {
                "mask": [
                    {
                        "masks": [[bool]],  # 2D boolean array representing the mask
                        "mask_ids": str,    # Unique identifier for the mask
                        "labels": int,      # Index of the label from `label_list`
                        "label_names": str, # Name of the label
                        "meta_data": [str], # List of metadata strings
                        "info_dict": {str: str}, # Dictionary of additional string-string pairs
                    }
                ],
                "mask_size": (int, int),  # Size of the resized image masks
                "image_size": (int, int), # Original dimensions of the input image
                "key": str                # Unique identifier for the returned value
            }
        
        - For auto_segmentation mode when a new bounding box is provided:
            {
                "new": {
                    "bbox": [
                        {
                            "bboxes": [list],   # Bbox coordinates in the specified format
                            "labels": int,      # Label index for the bbox
                            "label_names": str, # Label name for the bbox
                        }
                    ],
                    "bbox_format": str      # Format of the bounding box data
                },
                "mask": [List of mask objects],
                "mask_size": (int, int),  # Size of the resized image masks
                "image_size": (int, int), # Original dimensions of the input image
                "key": str                # Unique identifier for the returned value
            }
    """


    # Load Image and convert size
    image = Image.open(image_path)
    original_image_size = image.size
    image.thumbnail(size=(image_width, image_height))

    image_url = st_image.image_to_url(
        image,
        image.size[0],
        True,
        "RGB",
        "PNG",
        f"segmentation-{md5(image.tobytes()).hexdigest()}-{key}",
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

    # Configure default labels, meta_data
    num_masks = len(masks)
    if len(labels) > num_masks:
        labels = labels[:num_masks]
    else:
        labels.extend(["0"] * (num_masks - len(labels)))

    if len(meta_data) > num_masks:
        meta_data = meta_data[:num_masks]
    else:
        meta_data.extend([[]] * (num_masks - len(meta_data)))
        
    if len(info_dict) > num_masks:
        info_dict = info_dict[:num_masks]
    else:
        info_dict.extend([dict()] * (num_masks - len(info_dict)))
        
    if len(mask_ids) > num_masks:
        mask_ids = mask_ids[:num_masks]
    else:
        mask_ids.extend(["mask-" + str(i + len(mask_ids)) for i in range(num_masks - len(mask_ids))])
    
    mask_info = [
        {
            "data": item[0],
            "label": label_list[item[1]],
            "meta": item[2],
            "additional_data": item[3],
            "id": item[4],
        }
        for item in zip(masks, labels, meta_data, info_dict, mask_ids)
    ]
    
    _justify_content = {"left": "start", "center":"center", "right":"end"}[component_alignment]


    component_value = _component_func(
        image_url=image_url,
        image_size=image.size,
        label_list=label_list,
        masks_info=mask_info,
        color_map=color_map,
        line_width=line_width,
        ui_width=20,
        ui_height=20,
        edit_meta=_edit_meta,
        edit_description=_edit_description,
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
        label_type="segmentation",
        auto_seg_mode=auto_segmentation,
        justify_content=_justify_content,
    )
    
    _bboxes = []
    _masks = []
    
    if component_value is not None:    
        bboxes = component_value["new"]
        key = component_value["key"]
        masks = component_value["mask"]
                
        _bboxes = [
            {
                "bboxes": [b * scale for b in item["bbox"]],
                "labels": item["label_id"],
                "label_names": item["label"],
            }
            for item in bboxes
        ]
        
        # Convert back to original format
        if "REL" in bbox_format:
            bboxes = [
                convert_bbox_format(bbox["bboxes"], "XYWH", bbox_format.replace("REL_", ""))
                for bbox in _bboxes
            ]
            bboxes = [
                absolute_to_relative(bbox, original_image_size[0], original_image_size[1])
                for bbox in bboxes
            ]
        else:
            bboxes = [
                convert_bbox_format(bbox["bboxes"], "XYWH", bbox_format)
                for bbox in _bboxes
            ]
        for i in range(len(_bboxes)):
            _bboxes[i]["bboxes"] = bboxes[i]
        
        _masks = [
            {
                "masks": item["data"],
                "mask_ids" : item["id"],
                "labels": item["label_id"],
                "label_names": item["label"],
                "meta_data": item["meta"],
                "info_dict": item["additional_data"],
            }
            for item in masks
        ]
    
    if len(_bboxes) > 0:
        return {
            "new": {"bbox": _bboxes, "bbox_format": bbox_format},
            "mask": _masks,
            "mask_size": resized_image_size,
            "image_size": original_image_size,
            "key": key,
        }
    else:
        return {
                "mask": _masks,
                "mask_size": resized_image_size,
                "image_size": original_image_size,
                "key": key,
            }
