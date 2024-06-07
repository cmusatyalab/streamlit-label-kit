#
# Streamlit components for general labeling tasks
#
# Copyright (c) 2024 Carnegie Mellon University
# SPDX-License-Identifier: GPL-2.0-only
#

import streamlit as st
from glob import glob
from streamlit_label_kit import detection, annotation, segmentation, absolute_to_relative, convert_bbox_format, are_bboxes_equal

def wide_space_default():
    st.set_page_config(layout="wide")

wide_space_default()

mode = st.tabs(["Detection", "Classification", "Segmentation"])
label_list = ["deer", "human", "dog", "penguin", "flamingo", "teddy bear"]
image_path_list = glob("image/*.jpg")

image_size = [700, 467]
DEFAULT_HEIGHT = 512
DEFAULT_LINE_WIDTH = 1.0


with mode[0]:
    num_page = st.slider("page", 0, len(image_path_list) - 1, 1, key="slider_det")
    target_image_path = image_path_list[num_page]
    
    st.text("Configure Component")
    with st.expander("Image & Inputs"):
        c1, c2, = st.columns(2)
        with c1: _height = st.number_input("image_height (px)", min_value=0, value=DEFAULT_HEIGHT)
        with c2: _width = st.number_input("image_width (px)", min_value=0, value=DEFAULT_HEIGHT)
        
        _label_list = st.multiselect("Lable List", options=label_list, default=label_list)
        _bbox_show_label = st.toggle("bbox_show_label", True)
        
        c1, c2 = st.columns(2)
        with c1: _info_dict_help = st.toggle("Info Dict", help='value = [{"Confidence": 0.1, "testScore": 0.98}, {"Confidence": 0.2}]')
        with c2: _meta_help = st.toggle("MetaData/Description", help='value = [["meta/description1", "meta1", "meta2"], ["meta/description2"]]')
        if _meta_help:
            _meta = [["meta/description1", "meta1", "meta2"], ["meta/description2"]]
        else:
            _meta = []
        
        if _info_dict_help:
            _info_dict = [{"Confidence": 0.1, "testScore": 0.98}, {"Confidence": 0.2}]
            _bbox_show_info = st.toggle("bbox_show_info", True)
        else:
            _info_dict = []
            _bbox_show_info = False
            
        c1, c2 = st.columns(2)
        with c1: _bbox_format = st.selectbox("bbox_format", ["XYWH", "XYXY", "CXYWH", "REL_XYWH", "REL_XYXY", "REL_CXYWH"])
       
        
    with st.expander("Ui Size"):
        c1, c2, c3 = st.columns(3)
        with c1: _ui_size = st.selectbox("ui_size", ("small", "medium", "large"))
    
        c1, c2, c3 = st.columns(3)
        with c1: _ui_left_size = st.selectbox("ui_left_size", (None, "small", "medium", "large", "custom"))
        if _ui_left_size == "custom":
            with c2: _ui_left_size = st.number_input("left_size (px)", min_value=0, value=198)
        
        
        c1, c2, c3 = st.columns(3)
        with c1: _ui_bottom_size = st.selectbox("ui_bottom_size", (None, "small", "medium", "large", "custom"))
        if _ui_bottom_size == "custom":
            with c2: _ui_bottom_size = st.number_input("bottom_size (px)", min_value=0, value=198)
            
        c1, c2, c3 = st.columns(3)
        with c1: _ui_right_size = st.selectbox("ui_right_size", (None, "small", "medium", "large", "custom"))
        if _ui_right_size == "custom":
            with c2: _ui_right_size = st.number_input("right_size (px)", min_value=0, value=34)
        
    with st.expander("UI Setting & Position"):  
        c1, c2, c3 = st.columns(3)
        with c1: 
            _comp_alignment = st.selectbox("component_alignment", ("left", "center", "right"), key="compAlign_det")        
        
        c1, c2, c3 = st.columns(3)
        with c1: _ui_position = st.selectbox("ui_position", ("left", "right"))
        with c2: _line_width = st.number_input("line_width", min_value=0.5, value=DEFAULT_LINE_WIDTH, step=0.1)
        with c3: 
            _read_only = st.toggle("read_only", False)
    
    
        c1, c2, c3 = st.columns(3)
        with c1: _class_select_type = st.radio("class_select_type", ("select", "radio"))
        with c2: _class_select_position = st.selectbox("class_select_position", (None, "left", "right", "bottom"))
    
        c1, c2, c3 = st.columns(3)
        with c1: _item_editor = st.toggle("item_editor", False)
        if _item_editor:
            with c2: _item_editor_position = st.selectbox("item_editor_position", (None, "left", "right"))
            with c3: 
                _edit_description = st.toggle("edit_description")
                _edit_meta = st.toggle("edit_meta")
        else:
            _item_editor_position = None
            _edit_description = False
            _edit_meta = False
            
        c1, c2, c3 = st.columns(3)
        with c1: _item_selector = st.toggle("item_selector", False)
        if _item_selector:
            with c2: _item_selector_position = st.selectbox("item_selector_position", (None, "left", "right"))
        else:
            _item_selector_position = None
    
    _bbox = [[0, 0, 200, 100], [10, 20, 100, 150]]
    result_dict = {}
    _bbox_id =  ["bbox-" + str(i) for i in range(len(_bbox))]

    
    original_format = _bbox_format.replace("REL_", "")
    _bbox = [convert_bbox_format(bbox, "XYWH", original_format) for bbox in _bbox]
    if "REL" in _bbox_format:
        _bbox = [
            absolute_to_relative(bbox, image_size[0], image_size[1])
            for bbox in _bbox
        ]
        
    for img in image_path_list:
        result_dict[img] = {
            "bboxes": _bbox,
            "labels": [0, 0],
        }
    st.session_state["result"] = result_dict.copy()   
    
    # API
    function_args = [
        "\timage_path=image_path",
        f"label_list={_label_list}",
        f"bboxes={st.session_state['result'][target_image_path]['bboxes']}",
    ]

    if _bbox_id:
        function_args.append(f"bbox_ids={_bbox_id}")
        
    if _bbox_format != "XYWH":
        function_args.append(f"bbox_format={_bbox_format}")

    if _info_dict_help:
        function_args.append(f"info_dict={_info_dict}")

    if _meta_help:
        function_args.append(f"meta_data={_meta}")

    if _height != DEFAULT_HEIGHT:
        function_args.append(f"image_height={_height}")

    if _width != DEFAULT_HEIGHT:  # Assuming DEFAULT_WIDTH is the correct constant
        function_args.append(f"image_width={_width}")

    if _line_width != DEFAULT_LINE_WIDTH:
        function_args.append(f"line_width={_line_width}")

    if _ui_position != "left":
        function_args.append(f"ui_position={repr(_ui_position)}")

    if _class_select_position:
        function_args.append(f"class_select_position={repr(_class_select_position)}")

    if _item_editor_position:
        function_args.append(f"item_editor_position={repr(_item_editor_position)}")

    if _item_selector_position:
        function_args.append(f"item_selector_position={repr(_item_selector_position)}")

    if _class_select_type != "select":
        function_args.append(f"class_select_type={repr(_class_select_type)}")

    if _item_editor:
        function_args.append(f"item_editor={_item_editor}")

    if _item_selector:
        function_args.append(f"item_selector={_item_selector}")

    if _edit_description:
        function_args.append(f"edit_description={_edit_description}")

    if _edit_meta:
        function_args.append(f"edit_meta={_edit_meta}")

    if _ui_size != "small":
        function_args.append(f"ui_size={repr(_ui_size)}")

    if _ui_left_size:
        function_args.append(f"ui_left_size={repr(_ui_left_size)}")

    if _ui_bottom_size:
        function_args.append(f"ui_bottom_size={repr(_ui_bottom_size)}")

    if _ui_right_size:
        function_args.append(f"ui_right_size={repr(_ui_right_size)}")
        
    if _bbox_show_info:
        function_args.append(f"bbox_show_info={repr(_bbox_show_info)}")
        
    if _bbox_show_label:
        function_args.append(f"bbox_show_label={repr(_bbox_show_label)}")

    if _read_only:
        function_args.append(f"read_only={repr(_read_only)}")
    
    if _comp_alignment != "left":
        function_args.append(f"component_alignment={repr(_comp_alignment)}")

    function_args.append("key=None")
    final_function_call = "detection(\n" + ",\n\t".join(function_args) + "\n)"


    with st.expander("api"):
        st.code(f"result = {final_function_call}", language="python")
            

    st.text("Component")
    st.session_state.out = detection(
        image_path=target_image_path,
        bboxes=st.session_state["result"][target_image_path]["bboxes"],
        bbox_format=_bbox_format,
        bbox_ids=_bbox_id,
        labels=st.session_state["result"][target_image_path]["labels"],
        info_dict=_info_dict,
        meta_data=_meta,
        label_list=_label_list,
        line_width=_line_width,
        class_select_type=_class_select_type,
        item_editor=_item_editor,
        item_selector=_item_selector,
        edit_meta=_edit_meta,
        edit_description=_edit_description,
        ui_position=_ui_position,
        class_select_position=_class_select_position,
        item_editor_position=_item_editor_position,
        item_selector_position=_item_selector_position,
        image_height=_height,
        image_width=_width,
        ui_size=_ui_size,
        ui_left_size=_ui_left_size,
        ui_bottom_size=_ui_bottom_size,
        ui_right_size=_ui_right_size,
        bbox_show_info = _bbox_show_info,
        bbox_show_label = _bbox_show_label,
        read_only=_read_only,
        component_alignment=_comp_alignment,
    )
    
    st.text("Component Returns")
    st.session_state.out
    
    
           
    st.text("Other Examples")
 
    with st.expander("two-synchronized Example"):
        
        with st.echo():
            if "result_dup" not in st.session_state:
                st.session_state.result_dup = []
                
            if "result_dup_out1" not in st.session_state:
                st.session_state.result_dup_out1 = {"key": "", "bbox": []}
                
            if "result_dup_out2" not in st.session_state:
                st.session_state.result_dup_out2 = {"key": "", "bbox": []}
                
            data = st.session_state.result_dup or []
                                    
            bboxes = [item['bboxes'] for item in data]
            bbox_ids = [item['bbox_ids'] for item in data]
            labels = [item['labels'] for item in data]
            meta_data = [item['meta_data'] for item in data]
            info_dict = [item['info_dict'] for item in data]
            
            c1, c2 = st.columns(2)
            with c1: 
                test_out1 = detection(
                    image_path=target_image_path,
                    bboxes=bboxes,
                    bbox_ids=bbox_ids,
                    bbox_format=st.session_state.out["bbox_format"],
                    labels=labels,
                    info_dict=info_dict,
                    meta_data=meta_data,
                    label_list=_label_list,
                    line_width=_line_width,
                    class_select_type=_class_select_type,
                    ui_position="left",
                    item_editor=True,
                    # item_selector=True,
                    edit_meta=True,
                    bbox_show_label=True,
                    key="detection_dup1"
                )
                test_out1
            
            with c2:
                test_out2 = detection(
                    image_path=target_image_path,
                    bboxes=bboxes,
                    bbox_ids=bbox_ids,
                    bbox_format=st.session_state.out["bbox_format"],
                    labels=labels,
                    info_dict=info_dict,
                    meta_data=meta_data,
                    label_list=_label_list,
                    line_width=_line_width,
                    class_select_type=_class_select_type,
                    ui_position="right",
                    # item_editor=True,
                    item_selector=True,
                    edit_meta=True,
                    bbox_show_label=True,
                    key="detection_dup2"
                )
                test_out2
                    
            if (test_out1["key"] != st.session_state.result_dup_out1["key"] or test_out2["key"] != st.session_state.result_dup_out2["key"]):
                if test_out1["key"] != st.session_state.result_dup_out1["key"]:
                    st.session_state.result_dup_out1["key"] = test_out1["key"]
                    st.session_state.result_dup_out1["bbox"] = test_out1["bbox"]
                if test_out2["key"] != st.session_state.result_dup_out2["key"]:
                    st.session_state.result_dup_out2["key"] = test_out2["key"]
                    st.session_state.result_dup_out2["bbox"] = test_out2["bbox"]
                
                if st.session_state.result_dup_out2["key"] > st.session_state.result_dup_out1["key"]:  
                    st.session_state.result_dup = st.session_state.result_dup_out2["bbox"]
                else:
                    st.session_state.result_dup = st.session_state.result_dup_out1["bbox"]
                
                st.rerun()
            
    with st.expander("self-synchronized Example"):
        with st.echo():
            if "self_sync" not in st.session_state:
                st.session_state.self_sync = {"key": "", "bbox": []}
                
            data = st.session_state.self_sync["bbox"] or []
                                    
            bboxes = [item['bboxes'] for item in data]
            bbox_ids = [item['bbox_ids'] for item in data]
            labels = [item['labels'] for item in data]
            meta_data = [item['meta_data'] for item in data]
            info_dict = [item['info_dict'] for item in data]
            
            result = detection(
                image_path=target_image_path,
                bboxes=bboxes,
                bbox_ids=bbox_ids,
                bbox_format=st.session_state.out["bbox_format"],
                labels=labels,
                info_dict=info_dict,
                meta_data=meta_data,
                label_list=_label_list,
                key="self_sync_output"
            )
            
            if result["key"] != st.session_state.self_sync["key"]:
                st.session_state.self_sync["key"] = result["key"]
                st.session_state.self_sync["bbox"] = result["bbox"]
                
                st.rerun()   
            
        st.write('''
            #if you want to manipulate data do:\n
                st.session_state.self_sync["bbox"] = new_bbox_info\n
                st.rerun()
                    ''')

        st.session_state.self_sync 

        
with mode[1]: # Classification
    num_page = st.slider("page", 0, len(image_path_list) - 1, 1, key="slider_cls")
    _height = 512
    _width = 512
    _ui_height = 40
    _full_width = False
    
    st.text("Configure Component")
    with st.expander("Image & Inputs"):
        c1, c2, c3, = st.columns(3)
        with c1: _use_image = st.toggle("show image", True)
        if _use_image:
            with c2: _height = st.number_input("image_height (px)", min_value=0, value=512, key="annotation_height")
            with c3: _width = st.number_input("image_width (px)", min_value=0, value=512, key="annotation_weight")
        else :
            with c3: _ui_height = st.number_input("ui_height", min_value=0, value=40, key="annotation_ui_height")
            with c2: _full_width = st.toggle("ui_bottom_fill_width", False, key="annotation_full_width")
    
        
        _label_list = st.multiselect("Lable List", options=label_list, default=label_list, key="annotation_label_list")
        
    with st.expander("Ui Size"):
        c1, c2, c3 = st.columns(3)
        with c1: _ui_size = st.selectbox("ui_size", ("small", "medium", "large"), key="annotation_ui_size")

        c1, c2, c3 = st.columns(3)
        with c1: _ui_left_size = st.selectbox("ui_left_size", (None, "small", "medium", "large", "custom"), key="annotation_ui_left_size")
        if _ui_left_size == "custom":
            with c2: _ui_left_size = st.number_input("left_size (px)", min_value=0, value=198, key="annotation_left_size")
        
        
        c1, c2, c3 = st.columns(3)
        with c1: _ui_bottom_size = st.selectbox("ui_bottom_size", (None, "small", "medium", "large", "custom"), key="annotation_ui_botton_size")
        if _ui_bottom_size == "custom":
            with c2: _ui_bottom_size = st.number_input("bottom_size (px)", min_value=0, value=198)
            
        c1, c2, c3 = st.columns(3)
        with c1: _ui_right_size = st.selectbox("ui_right_size", (None, "small", "medium", "large", "custom"), key="annotation_ui_right_size")
        if _ui_right_size == "custom":
            with c2: _ui_right_size = st.number_input("right_size (px)", min_value=0, value=34)
    
    with st.expander("UI Setting & Position"): 
        c1, c2, c3 = st.columns(3)
        with c1: _comp_alignment = st.selectbox("component_alignment", ("left", "center", "right"), key="compAlign_anno")        
               
        c1, c2, c3 = st.columns(3)
        with c1: _ui_position = st.selectbox("ui_position", ("left", "right"), key="annotation_item_editor_pos")
        with c3: _read_only = st.toggle("read_only", False, "read_only_classification")
    
        c1, c2, c3 = st.columns(3)
        with c1: _classification = st.toggle("classification", True, key="annotation_classification")
        if _classification:
            with c2: _class_select_position = st.selectbox("class_select_position", (None, "left", "right", "bottom"), key="annotation_class_select_position")
            with c3: _class_select_type = st.radio("class_select_type", ("select", "radio"), key="annotation_class_select_type")
            with c1: _multi = st.toggle("multi_select", False)
        else:
            _multi = False
            _class_select_type = "select"
            _class_select_position = None
    
        c1, c2, c3 = st.columns(3)
        with c1: _meta_editor = st.toggle("meta_editor", True, key="annotation_meta_editor")
        if _meta_editor:
            with c2: _meta_editor_position = st.selectbox("meta_editor_position", (None, "left", "right"), key="annotation_meta_editor_position")
            with c3: _edit_description = st.toggle("edit_description", key="annotation_editDescription")
        else:
            _meta_editor_position = None
            _edit_description = False
    
    function_args = [
        f"label_list={_label_list}",
        "label_index=0" 
    ]
    
    if _use_image:
        function_args.append("image_path=image_path")
        
        if _height != DEFAULT_HEIGHT:
            function_args.append(f"image_height={_height}")

        if _width != DEFAULT_HEIGHT:  # Assuming DEFAULT_WIDTH is the correct constant
            function_args.append(f"image_width={_width}")
    
    else:
        if _full_width:
            function_args.append(f"ui_bottom_fill_width={repr(_full_width)}")
            
        function_args.append(f"ui_height={repr(_ui_height)}")  
        
    if _classification:
        function_args.append(f"classification={_classification}")
    
    if _multi:
        function_args.append(f"multi_select={_multi}")
        
    if _ui_position != "left":
        function_args.append(f"ui_position = {repr(_ui_position)}")
    
    if _class_select_position:
        function_args.append(f"class_select_position = {repr(_class_select_position)}")
    
    if _meta_editor_position:
        function_args.append(f"meta_editor_position = {repr(_meta_editor_position)}")
        
    if _class_select_type != "radio":
        function_args.append(f"class_select_position = {repr(_class_select_type)}")
        
    if _meta_editor:
        function_args.append(f"meta_editor = {repr(_meta_editor)}")
        
    if _edit_description:
        function_args.append(f"edit_description = {repr(_edit_description)}")
    
    if _ui_size != "small":
        function_args.append(f"ui_size={repr(_ui_size)}")

    if _ui_left_size:
        function_args.append(f"ui_left_size={repr(_ui_left_size)}")

    if _ui_bottom_size:
        function_args.append(f"ui_bottom_size={repr(_ui_bottom_size)}")

    if _ui_right_size:
        function_args.append(f"ui_right_size={repr(_ui_right_size)}")
    
    if _read_only:
        function_args.append(f"read_only={repr(_read_only)}")
    
    if _comp_alignment != "left":
        function_args.append(f"component_alignment={repr(_comp_alignment)}")
    
    function_args.append("key=None")
    final_function_call = "annotation(\n" + ",\n\t".join(function_args) + "\n)"

    with st.expander("api"):
        st.code(f"result = {final_function_call}", language="python")    

    st.write("component")
    label = annotation(
        image_path=image_path_list[num_page] if _use_image else None,
        label_list=_label_list,
        label_index=0,
        image_height=_height,
        image_width=_width,
        classification=_classification,
        multi_select=_multi,
        ui_position = _ui_position,
        class_select_position = _class_select_position,
        meta_editor_position = _meta_editor_position,
        class_select_type = _class_select_type,
        meta_editor = _meta_editor,
        edit_description = _edit_description,    
        ui_size = _ui_size,
        ui_left_size = _ui_left_size,
        ui_bottom_size = _ui_bottom_size,
        ui_right_size = _ui_right_size,
        ui_bottom_fill_width = _full_width,
        ui_height = _ui_height,
        read_only=_read_only,
        component_alignment=_comp_alignment,
        key=None,
    )
    
    st.write("component returns")
    label
    
    st.text("Other Examples")
 
    with st.expander("two-synchronized Example"):
        
        with st.echo():
            if "class_dup" not in st.session_state:
                st.session_state.class_dup = []
                
            if "class_dup_out1" not in st.session_state:
                st.session_state.class_dup_out1 = {"key": "", "label": "", "meta": []}
                
            if "class_dup_out2" not in st.session_state:
                st.session_state.class_dup_out2 = {"key": "", "label": "", "meta": []}
                
            _label = st.session_state.class_dup or {"key": "", "label": "", "meta": []}
                       
            try:
                index = _label_list.index(_label["label"])
            except ValueError:
                index = 0        
            label_index = index
            meta_data = _label["meta"]
            
            c1, c2 = st.columns(2)
            with c1: 
                class_out1 = annotation(
                    image_path=image_path_list[num_page] if _use_image else None,
                    label_list=_label_list,
                    label_index=label_index,
                    meta_data=meta_data,
                    image_height=_height,
                    image_width=_width,
                    classification=True,
                    class_select_type = _class_select_type,
                    meta_editor = True,
                    key="class_dup1",
                ) or {"key": "", "label": "", "meta": []}
                class_out1
            
            with c2:
                class_out2 = annotation(
                    image_path=image_path_list[num_page] if _use_image else None,
                    label_list=_label_list,
                    label_index=label_index,
                    meta_data=meta_data,
                    image_height=_height,
                    image_width=_width,
                    classification=True,
                    class_select_type = _class_select_type,
                    meta_editor = True,
                    key="class_dup2",
                ) or {"key": "", "label": "", "meta": []}
                class_out2
            
                    
            if (class_out1["key"] != st.session_state.class_dup_out1["key"] or class_out2["key"] != st.session_state.class_dup_out2["key"]):
                if class_out1["key"] != st.session_state.class_dup_out1["key"]:
                    st.session_state.class_dup_out1 = class_out1
                if class_out2["key"] != st.session_state.class_dup_out2["key"]:
                    st.session_state.class_dup_out2 = class_out2
                
                if st.session_state.class_dup_out2["key"] > st.session_state.class_dup_out1["key"]:  
                    st.session_state.class_dup = st.session_state.class_dup_out2
                else:
                    st.session_state.class_dup = st.session_state.class_dup_out1
                
                st.rerun()
                
        st.write('''
            #WARNNING:\n
                If you are "inputing" data to "annotation", always provide appropriate value to the "meta_data" argument
            ''')

with mode[2]: #Segmentation
    num_page = st.slider("page", 0, len(image_path_list) - 1, 1, key="slider_seg")
    target_image_path = image_path_list[num_page]
    
    st.text("Configure Component")
    with st.expander("Image & Inputs"):
        c1, c2, = st.columns(2)
        with c1: _height = st.number_input("image_height (px)", min_value=0, value=DEFAULT_HEIGHT, key="ih_seg")
        with c2: _width = st.number_input("image_width (px)", min_value=0, value=DEFAULT_HEIGHT, key="iw_seg")
        
        _label_list = st.multiselect("Lable List", options=label_list, default=label_list, key="ll_seg")
        
        c1, c2 = st.columns(2)
        with c1: _info_dict_help = st.toggle("Info Dict", help='value = [{"Confidence": 0.1, "testScore": 0.98}, {"Confidence": 0.2}]', key="id_seg")
        with c2: _meta_help = st.toggle("MetaData/Description", help='value = [["meta/description1", "meta1", "meta2"], ["meta/description2"]]', key="meta_descrip_seg")
        if _meta_help:
            _meta = [["meta/description1", "meta1", "meta2"], ["meta/description2"]]
        else:
            _meta = []
        
        if _info_dict_help:
            _info_dict = [{"Confidence": 0.1, "testScore": 0.98}, {"Confidence": 0.2}]
        else:
            _info_dict = []
            
        c1, c2 = st.columns(2)
        with c1: _auto_segmentation = st.toggle("auto_segmentation", False)
        if _auto_segmentation:
            with c2: _bbox_format = st.selectbox("bbox_format", ["XYWH", "XYXY", "CXYWH", "REL_XYWH", "REL_XYXY", "REL_CXYWH"], key="bbf_seg")
        else: 
            _bbox_format = "XYWH"
        
    with st.expander("Ui Size"):
        c1, c2, c3 = st.columns(3)
        with c1: _ui_size = st.selectbox("ui_size", ("small", "medium", "large"), key="uis_seg")
    
        c1, c2, c3 = st.columns(3)
        with c1: _ui_left_size = st.selectbox("ui_left_size", (None, "small", "medium", "large", "custom"), key="uils_seg")
        if _ui_left_size == "custom":
            with c2: _ui_left_size = st.number_input("left_size (px)", min_value=0, value=198, key="ls_seg")
        
        
        c1, c2, c3 = st.columns(3)
        with c1: _ui_bottom_size = st.selectbox("ui_bottom_size", (None, "small", "medium", "large", "custom"), key="uibs_seg")
        if _ui_bottom_size == "custom":
            with c2: _ui_bottom_size = st.number_input("bottom_size (px)", min_value=0, value=198, key="bs_seg")
            
        c1, c2, c3 = st.columns(3)
        with c1: _ui_right_size = st.selectbox("ui_right_size", (None, "small", "medium", "large", "custom"), key="uirs_seg")
        if _ui_right_size == "custom":
            with c2: _ui_right_size = st.number_input("right_size (px)", min_value=0, value=34, key="rs_seg")
        
    with st.expander("UI Setting & Position"):                
        c1, c2, c3 = st.columns(3)
        with c1: _comp_alignment = st.selectbox("component_alignment", ("left", "center", "right"), key="compAlign_seg")        

        c1, c2, c3 = st.columns(3)
        with c1: _ui_position = st.selectbox("ui_position", ("left", "right"), key="uip_seg")
        
        with c3: _read_only = st.toggle("read_only", False, "rdo_seg")
    
    
        c1, c2, c3 = st.columns(3)
        with c1: _class_select_position = st.selectbox("class_select_position", (None, "left", "right", "bottom"), key="csp_seg")
    
        c1, c2, c3 = st.columns(3)
        with c1: _item_editor = st.toggle("item_editor", False, key="ie_seg")
        if _item_editor:
            with c2: _item_editor_position = st.selectbox("item_editor_position", (None, "left", "right"), key="iep_seg")
            with c3: 
                _edit_description = st.toggle("edit_description", key="ed_seg")
                _edit_meta = st.toggle("edit_meta", key="em_seg")
        else:
            _item_editor_position = None
            _edit_description = False
            _edit_meta = False
            
        c1, c2, c3 = st.columns(3)
        with c1: _item_selector = st.toggle("item_selector", False, key="is_seg")
        if _item_selector:
            with c2: _item_selector_position = st.selectbox("item_selector_position", (None, "left", "right"), key="isp_seg")
        else:
            _item_selector_position = None
    
    function_args = [
        "\timage_path=image_path",
        f"label_list={_label_list}",
        f"masks=[] #list of 2d array",
        f"mask_ids=[]",
    ]
    if _info_dict_help:
        function_args.append(f"info_dict={_info_dict}")

    if _meta_help:
        function_args.append(f"meta_data={_meta}")

    if _height != DEFAULT_HEIGHT:
        function_args.append(f"image_height={_height}")

    if _width != DEFAULT_HEIGHT:  # Assuming DEFAULT_WIDTH is the correct constant
        function_args.append(f"image_width={_width}")

    if _ui_position != "left":
        function_args.append(f"ui_position={repr(_ui_position)}")

    if _class_select_position:
        function_args.append(f"class_select_position={repr(_class_select_position)}")

    if _item_editor_position:
        function_args.append(f"item_editor_position={repr(_item_editor_position)}")

    if _item_selector_position:
        function_args.append(f"item_selector_position={repr(_item_selector_position)}")

    if _item_editor:
        function_args.append(f"item_editor={_item_editor}")

    if _item_selector:
        function_args.append(f"item_selector={_item_selector}")

    if _edit_description:
        function_args.append(f"edit_description={_edit_description}")

    if _edit_meta:
        function_args.append(f"edit_meta={_edit_meta}")

    if _ui_size != "small":
        function_args.append(f"ui_size={repr(_ui_size)}")

    if _ui_left_size:
        function_args.append(f"ui_left_size={repr(_ui_left_size)}")

    if _ui_bottom_size:
        function_args.append(f"ui_bottom_size={repr(_ui_bottom_size)}")

    if _ui_right_size:
        function_args.append(f"ui_right_size={repr(_ui_right_size)}")

    if _read_only:
        function_args.append(f"read_only={repr(_read_only)}")

    if _auto_segmentation:
        function_args.append(f"auto_segmentation={repr(_auto_segmentation)}")
        
        if _bbox_format != "XYWH":
            function_args.append(f"bbox_format={_bbox_format}")
        
    if _comp_alignment != "left":
        function_args.append(f"component_alignment={repr(_comp_alignment)}")
        
    function_args.append("key=None")
    final_function_call = "segmentation(\n" + ",\n\t".join(function_args) + "\n)"

    # Usage example with st.code
    with st.expander("api"):
        st.code(f"result = {final_function_call}", language="python")
     
    st.write("component")
    st.session_state.out = segmentation(
        image_path=target_image_path,
        bbox_format=_bbox_format,
        masks=[],
        mask_ids=[],
        labels=[],
        info_dict=_info_dict,
        meta_data=_meta,
        label_list=_label_list,
        item_editor=_item_editor,
        item_selector=_item_selector,
        edit_meta=_edit_meta,
        edit_description=_edit_description,
        ui_position=_ui_position,
        class_select_position=_class_select_position,
        item_editor_position=_item_editor_position,
        item_selector_position=_item_selector_position,
        image_height=_height,
        image_width=_width,
        ui_size=_ui_size,
        ui_left_size=_ui_left_size,
        ui_bottom_size=_ui_bottom_size,
        ui_right_size=_ui_right_size,
        read_only=_read_only,
        auto_segmentation = _auto_segmentation,
        component_alignment=_comp_alignment,
    )
    
    st.write("component returns")
    st.session_state.out
    
    st.text("Other Examples")
    
    with st.expander("two-synchronized Example"):
        
        with st.echo():
            if "seg_dup" not in st.session_state:
                st.session_state.seg_dup = []
                
            if "seg_dup_out1" not in st.session_state:
                st.session_state.seg_dup_out1 = {"key": "", "mask": []}
                
            if "seg_dup_out2" not in st.session_state:
                st.session_state.seg_dup_out2 = {"key": "", "mask": []}
                
            data = st.session_state.seg_dup or []
                       
            masks = [item['masks'] for item in data]
            mask_ids = [item['mask_ids'] for item in data]
            labels = [item['labels'] for item in data]
            meta_data = [item['meta_data'] for item in data]
            info_dict = [item['info_dict'] for item in data]
            
            c1, c2 = st.columns(2)
            with c1: 
                seg_out1 = segmentation(
                    image_path=target_image_path,
                    bbox_format=_bbox_format,
                    masks=masks,
                    mask_ids=mask_ids,
                    labels=labels,
                    meta_data=meta_data,
                    label_list=_label_list,
                    item_editor=True,
                    # item_selector=False,
                    edit_meta=True,
                    key="seg_dup1",
                ) or {"key": "", "mask":[]}
                # seg_out1
            
            with c2:
                seg_out2 = segmentation(
                    image_path=target_image_path,
                    bbox_format=_bbox_format,
                    masks=masks,
                    mask_ids=mask_ids,
                    labels=labels,
                    ui_position="right",
                    meta_data=meta_data,
                    label_list=_label_list,
                    item_editor=True,
                    item_selector=True,
                    edit_meta=True,
                    key="seg_dup2",
                ) or {"key": "", "mask":[]}
                # seg_out2
            
                    
            if (seg_out1["key"] != st.session_state.seg_dup_out1["key"] or seg_out2["key"] != st.session_state.seg_dup_out2["key"]):
                if seg_out1["key"] != st.session_state.seg_dup_out1["key"]:
                    st.session_state.seg_dup_out1 = seg_out1
                if class_out2["key"] != st.session_state.seg_dup_out2["key"]:
                    st.session_state.seg_dup_out2 = seg_out2
                
                if st.session_state.seg_dup_out2["key"] > st.session_state.seg_dup_out1["key"]:  
                    st.session_state.seg_dup = st.session_state.seg_dup_out2["mask"]
                else:
                    st.session_state.seg_dup = st.session_state.seg_dup_out1["mask"]
                
                st.rerun()
                