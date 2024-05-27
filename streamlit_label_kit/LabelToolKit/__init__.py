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
from streamlit_label_kit import IS_RELEASE
from typing import Literal

if IS_RELEASE:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(absolute_path, "frontend/build")
    _component_func = components.declare_component("st-label-kit", path=build_path)
else:
    _component_func = components.declare_component(
        "st-label-kit", url="http://localhost:3000"
    )

def get_colormap(label_names, colormap_name="gist_rainbow"):
    colormap = {}
    cmap = plt.get_cmap(colormap_name)
    for idx, l in enumerate(label_names):
        rgb = [int(d) for d in np.array(cmap(float(idx) / len(label_names))) * 255][:3]
        colormap[l] = "#%02x%02x%02x" % tuple(rgb)
    return colormap

SELECT_HEIGHT = 60
RADIO_HEGIHT = 34
UI_WIDTH = 198

#'''
# bboxes:
# [[x,y,w,h],[x,y,w,h]]
# labels:
# [0,3]
#'''

# def detection(
#     image_path,
#     label_list,
#     bboxes=None,
#     labels=None,
#     height=512,
#     width=512,
#     line_width=1.0,
#     controller_size: Literal["small", "middle", "large"] = "small",
#     key=None,
# ) -> CustomComponent:
#     image = Image.open(image_path)
#     original_image_size = image.size
#     image.thumbnail(size=(width, height))
#     resized_image_size = image.size
#     scale = original_image_size[0] / resized_image_size[0]

#     image_url = st_image.image_to_url(
#         image,
#         image.size[0],
#         True,
#         "RGB",
#         "PNG",
#         f"annotation-{md5(image.tobytes()).hexdigest()}-{key}",
#     )
#     if image_url.startswith("/"):
#         image_url = image_url[1:]

#     color_map = get_colormap(label_list, colormap_name="gist_rainbow")
#     bbox_info = [
#         {
#             "bbox": [b / scale for b in item[0]],
#             "label_id": item[1],
#             "label": label_list[item[1]],
#         }
#         for item in zip(bboxes, labels)
#     ]
    
#     ui_height = RADIO_HEGIHT
#     ui_width = UI_WIDTH
#     match controller_size:
#         case "small":
#             ui_height = ui_height
#             ui_width = ui_width
#         case "middle":
#             ui_height = int(2 * ui_height)
#             ui_width = int(1.25 * ui_width)
#         case "large":
#             ui_height = int(4 * ui_height)
#             ui_width = int(1.5 * ui_width)
    
#     component_value = _component_func(
#         image_url=image_url,
#         image_size=image.size,
#         label_list=label_list,
#         bbox_info=bbox_info,
#         color_map=color_map,
#         line_width=line_width,
#         ui_width=ui_width,
#         ui_height=RADIO_HEGIHT,
#         key=key,
#         label_type="detection"
#     )
#     bbox = None
#     if component_value is not None:
#         bbox = component_value["bbox"]
        
#         bbox = [
#             {
#                 "bbox": [b * scale for b in item["bbox"]],
#                 "label_id": item["label_id"],
#                 "label": item["label"],
#                 "meta": item["meta"],
#             }
#             for item in bbox
#         ]
#     return bbox

# def classification(
#     image_path: str,
#     label_list: list[str],
#     default_label_index: int=None,
#     height: int=512,
#     width: int=512,
#     layout: Literal["horizontal", "vertical"] = "horizontal",
#     select_list: bool = False,
#     multi_select: bool = False,
#     controller_size: Literal["small", "middle", "large"] = "small",
#     key=None,
# ) -> CustomComponent:
#     image = Image.open(image_path)
#     image.thumbnail(size=(width, height))
#     image_url = st_image.image_to_url(
#         image,
#         image.size[0],
#         True,
#         "RGB",
#         "PNG",
#         f"classification-{md5(image.tobytes()).hexdigest()}-{key}",
#     )
#     if image_url.startswith("/"):
#         image_url = image_url[1:]
        
#     if multi_select and isinstance(default_label_index, list):
#         default_label_list = [label_list[i] for i in default_label_index]
#     else:
#         default_label_list = []
    
#     ui_height = RADIO_HEGIHT
#     ui_width = UI_WIDTH
#     match controller_size:
#         case "small":
#             ui_height = ui_height
#             ui_width = ui_width
#         case "middle":
#             ui_height = int(2 * ui_height)
#             ui_width = int(1.25 * ui_width)
#         case "large":
#             ui_height = int(4 * ui_height)
#             ui_width = int(1.5 * ui_width)
    
#     if layout == "vertical" and select_list:
#         ui_height = SELECT_HEIGHT
        
#     component_value = _component_func(
#         image_url=image_url,
#         image_size=image.size,
#         label_list=label_list,
#         ui_height=ui_height,
#         ui_width=ui_width,
#         default_label_idx=default_label_index,
#         key=key,
#         vertical_layout=(layout == "vertical"),
#         select_list=select_list,
#         multi_select=multi_select,
#         default_multi_label_list=default_label_list,
#         label_type="classification"
#     )
    
#     # component_value = _component_func(
#     #     image_url=image_url,
#     #     image_size=image.size,
#     #     label_list=label_list,
#     #     ui_width=ui_width,
#     #     ui_height=RADIO_HEGIHT,
#     #     key=image_url,
#     #     label_type="detection"
#     # )
#     return component_value
