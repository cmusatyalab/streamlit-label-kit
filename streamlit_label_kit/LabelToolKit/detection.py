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


def detection(
    image_path,
    label_list,
    bboxes=None,
    labels=[],
    read_only=False,
    infoDict={},
    metaDatas: list[list[str]] = [],
    bbox_format: Literal["XYWH", "XYXY", "CXYWH", "REL_XYWH", "REL_XYXY"] = "XYWH",
    image_height=512,
    image_width=512,
    line_width=1.0,
    ui_position: Literal["right", "left"] = "right",
    class_select_position: Literal["right", "left", "bottom"] = None,
    item_editor_position: Literal["right", "left"] = None,
    item_selector_position: Literal["right", "left"] = None,
    class_select_type: Literal["select", "radio"] = "select",
    item_editor: bool = True,
    item_selector: bool = True,
    edit_meta: bool = True,
    edit_description: bool = False,
    ui_size: Literal["small", "medium", "large"] = "small",
    ui_left_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_bottom_size: Union[Literal["small", "medium", "large"], int] = None,
    ui_right_size: Union[Literal["small", "medium", "large"], int] = None,
    key=None,
) -> CustomComponent:

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
    _edit_meta = not edit_description

    _, _left_size = _calc_size(ui_left_size or ui_size)
    _bottom_size, _ = _calc_size(ui_bottom_size or ui_size)
    _, _right_size = _calc_size(ui_right_size or ui_size)

    _select_type = "radio" if class_select_type != "select" else "select"

    # Configure default labels, metaDatas
    num_bboxes = len(bboxes)
    if len(labels) > num_bboxes:
        labels = labels[:num_bboxes]
    else:
        labels.extend(["0"] * (num_bboxes - len(labels)))

    if len(metaDatas) > num_bboxes:
        metaDatas = metaDatas[:num_bboxes]
    else:
        metaDatas.extend([[]] * (num_bboxes - len(metaDatas)))

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
            "label_id": item[1],
            "label": label_list[item[1]],
            "meta": item[2],
        }
        for item in zip(bboxes, labels, metaDatas)
    ]

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
        read_only=read_only,
        label_type="detection",
    )
    
    bboxes = None
    if component_value is not None:
        bboxes = component_value["bbox"]
        bboxes = [
            {
                "bbox": [b * scale for b in item["bbox"]],
                "label_id": item["label_id"],
                "label": item["label"],
                "meta": item["meta"],
            }
            for item in bboxes
        ]

        # Convert back to original format
        if "REL" in bbox_format:
            bboxes = [
                convert_bbox_format(bbox["bbox"], "XYWH", original_format)
                for bbox in bboxes
            ]
            bboxes = [
                absolute_to_relative(bbox, original_image_size[0], original_image_size[1])
                for bbox in bboxes
            ]
        else:
            bboxes = [
                convert_bbox_format(bbox["bbox"], "XYWH", original_format)
                for bbox in bboxes
            ]

    return {
        "bbox": bboxes,
        "image_size": original_image_size,
    }
