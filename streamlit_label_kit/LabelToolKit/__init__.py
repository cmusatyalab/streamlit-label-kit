#
# Streamlit components for general labeling tasks
#
# Copyright (c) 2024 Carnegie Mellon University
# SPDX-License-Identifier: GPL-2.0-only
#

from pathlib import Path

import streamlit.components.v1 as components
from typing import Literal, Tuple
from PIL import Image



build_path = Path(__file__).resolve().parent.joinpath("frontend", "build")
_component_func = components.declare_component("st-label-kit", path=str(build_path))


def convert_bbox_format(
    bbox: Tuple[float, float, float, float],
    input_format: Literal["XYWH", "XYXY", "CXYWH"],
    output_format: Literal["XYWH", "XYXY", "CXYWH"],
) -> Tuple[float, float, float, float]:
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
    bbox: Tuple[float, float, float, float], image_width: int, image_height: int
) -> Tuple[float, float, float, float]:
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
    bbox: Tuple[float, float, float, float], image_width: int, image_height: int
) -> Tuple[float, float, float, float]:
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

def thumbnail_with_upscale(image: Image, size : Tuple[int, int]) -> Image:
    """
    Imitates PIL's image.thumbnail function, but supports upscaling while preserving aspect ratio

    Args:
    image (PIL.Image): The image to be resized
    size (Tuple[int, int]): The desired target size (width, height)

    Returns:
    PIL.Image: The resized image
    """
    original_width, original_height = image.size
    target_width, target_height = size
    

    aspect_ratio = original_width / original_height
    new_width = target_width
    new_height = int(target_width / aspect_ratio)

    if new_height > target_height:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    return image.resize((new_width, new_height), Image.LANCZOS)