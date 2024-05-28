import streamlit as st
from glob import glob
import pandas as pd
from streamlit_label_kit import detection, annotation, segmentation

mode = st.tabs(["Detection", "Classification", "Segmentation"])
label_list = ["deer", "human", "dog", "penguin", "flamingo", "teddy bear"]
image_path_list = glob("image/*.jpg")

image_size = [700, 467]

with mode[0]:
    
    if "result" not in st.session_state:
        result_dict = {}
        for img in image_path_list:
            # # XYWH format
            # result_dict[img] = {
            #     "bboxes": [[0, 0, 200, 100], [10, 20, 100, 150]],
            #     "labels": [0, 0],
            # }
            
            # # REL_XYWH format
            # result_dict[img] = {
            #     "bboxes": [
            #         [0 / image_size[0], 0 / image_size[1], 200 / image_size[0], 100 / image_size[1]], 
            #         [10 /image_size[0], 20 / image_size[1], 100 / image_size[0], 150 / image_size[1]]
            #         ],
            #     "labels": [0, 0],
            # }
            
            # # XYXY format
            # result_dict[img] = {
            #     "bboxes": [[0, 0, 200, 100], [10, 20, 110, 170]],
            #     "labels": [0, 0],
            # }
            
            # # REL_XYXY format
            result_dict[img] = {
                "bboxes": [
                    [0 / image_size[0], 0 / image_size[1], 200 / image_size[0], 100 / image_size[1]], 
                    [10 /image_size[0], 20 / image_size[1], 110 / image_size[0], 170 / image_size[1]]
                    ],
                "labels": [0, 0],
            }
        st.session_state["result"] = result_dict.copy()

    num_page = st.slider("page", 0, len(image_path_list) - 1, 1, key="slider_det")
    target_image_path = image_path_list[num_page]
    
    with st.expander("Size & Label List"):
        c1, c2, = st.columns(2)
        with c1: _height = st.number_input("image_height (px)", min_value=0, value=512)
        with c2: _width = st.number_input("image_width (px)", min_value=0, value=512)
        
        _label_list = st.multiselect("Lable List", options=label_list, default=label_list)
        
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
        with c1: _ui_position = _item_editor_position = st.selectbox("ui_position", ("left", "right"))
        with c2: _line_width = st.number_input("line_width", min_value=0.5, value=1.0, step=0.1)
    
    
        c1, c2, c3 = st.columns(3)
        with c1: _class_select_type = st.selectbox("class_select_type", ("select", "radio"))
        with c2: _class_select_position = st.selectbox("class_select_position", (None, "left", "right", "bottom"))
    
        c1, c2, c3 = st.columns(3)
        with c1: _item_editor = st.toggle("item_editor", True)
        if _item_editor:
            with c2: _item_editor_position = st.selectbox("item_editor_position", (None, "left", "right"))
            with c3: _edit_description = st.toggle("edit_description")
        else:
            _item_editor_position = None
            _edit_description = False
            
        c1, c2, c3 = st.columns(3)
        with c1: _item_selector = st.toggle("item_selector", True)
        if _item_selector:
            with c2: _item_selector_position = st.selectbox("item_selector_position", (None, "left", "right"))
        else:
            _item_selector_position = None
    
    st.session_state.out = detection(
        image_path=target_image_path,
        bboxes=st.session_state["result"][target_image_path]["bboxes"],
        bbox_format="REL_XYXY",
        labels=st.session_state["result"][target_image_path]["labels"],
        label_list=_label_list,
        line_width=_line_width,
        class_select_type=_class_select_type,
        item_editor=_item_editor,
        item_selector=_item_selector,
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
    )
    st.session_state.out
    
    with st.expander("api"):
        st.code(f'''result = detection(
        image_path=image_path,
        label_list={_label_list},
        bboxes={st.session_state["result"][target_image_path]["bboxes"]},
        bbox_format='REL_XYXY'
        labels={st.session_state["result"][target_image_path]["labels"]},
        metaDatas=[],
        height={_height},
        width={_width},
        line_width={_line_width},
        ui_position={repr(_ui_position)},
        class_select_position={repr(_class_select_position)},
        item_editor_position={repr(_item_editor_position)},
        item_selector_position={repr(_item_selector_position)},
        class_select_type={repr(_class_select_type)},
        item_editor={_item_editor},
        item_selector={_item_selector},
        edit_description={_edit_description},
        ui_size={repr(_ui_position)},
        ui_left_size={repr(_ui_left_size)},
        ui_bottom_size={repr(_ui_bottom_size)},
        ui_right_size={repr(_ui_right_size)},
        key=None
    )''', language="python")
    
    
with mode[1]: # Classification
    num_page = st.slider("page", 0, len(image_path_list) - 1, 1, key="slider_cls")
    _height = 512
    _width = 512
    _ui_height = 40
    _full_width = False
    
    with st.expander("Size & Label List"):
        c1, c2, c3, = st.columns(3)
        with c1: _use_image = st.toggle("show image", True)
        if _use_image:
            with c2: _height = st.number_input("image_height (px)", min_value=0, value=512, key="annotation_height")
            with c3: _width = st.number_input("image_width (px)", min_value=0, value=512, key="annotation_weight")
        else :
            with c3: _ui_height = st.number_input("ui_height", min_value=0, value=40, key="annotation_ui_height")
            with c2: _full_width = st.toggle("ui_bottom_fill_width", False, key="annotation_full_width")
    
        
        _label_list = st.multiselect("Lable List", options=label_list, default=label_list, key="annotation_label_list")
        
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
        with c1: _ui_position = _item_editor_position = st.selectbox("ui_position", ("left", "right"), key="annotation_item_editor_pos")
    
        c1, c2, c3, c4 = st.columns(4)
        with c1: _classification = st.toggle("classification", True, key="annotation_classification")
        if _classification:
            with c2: _class_select_position = st.selectbox("class_select_position", (None, "left", "right", "bottom"), key="annotation_class_select_position")
            with c3: _class_select_type = st.selectbox("class_select_type", ("select", "radio"), key="annotation_class_select_type")
            with c4: _multi = st.toggle("multi_select", False)
        else:
            _multi = False
            _class_select_type = "select"
            _class_select_position = None
    
        c1, c2, c3, c4 = st.columns(4)
        with c1: _meta_editor = st.toggle("meta_editor", True, key="annotation_meta_editor")
        if _meta_editor:
            with c2: _meta_editor_position = st.selectbox("meta_editor_position", (None, "left", "right"), key="annotation_meta_editor_position")
            with c3: _edit_description = st.toggle("edit_description", key="annotation_editDescription")
        else:
            _meta_editor_position = None
            _edit_description = False
                          
    label = annotation(
        image_path=image_path_list[num_page] if _use_image else None,
        label_list=_label_list,
        default_label_index=0,
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
        
        key=None,
    )
    
    label
    
    with st.expander("api"):
        st.code(f'''result = annotation(
        image_path=image_path,
        label_list={_label_list},
        default_label_index=0,        
        image_height={_height},
        image_width={_width},
        classification={_classification},
        multi_select={_multi},
        ui_position = {repr(_ui_position)},
        class_select_position = {repr(_class_select_position)},
        meta_editor_position = {repr(_meta_editor_position)},
        
        class_select_type = {repr(_class_select_type)},
        meta_editor = {repr(_meta_editor)},
        edit_description = {repr(_edit_description)},
            
        ui_size={repr(_ui_position)},
        ui_left_size={repr(_ui_left_size)},
        ui_bottom_size={repr(_ui_bottom_size)},
        ui_right_size={repr(_ui_right_size)},
        
        fill_width = {_full_width},
        ui_height = {_ui_height},
        
        key=None,
    )''', language="python")

with mode[2]:
    
    if "result" not in st.session_state:
        result_dict = {}
        for img in image_path_list:
            # # XYWH format
            # result_dict[img] = {
            #     "bboxes": [[0, 0, 200, 100], [10, 20, 100, 150]],
            #     "labels": [0, 0],
            # }
            
            # # REL_XYWH format
            # result_dict[img] = {
            #     "bboxes": [
            #         [0 / image_size[0], 0 / image_size[1], 200 / image_size[0], 100 / image_size[1]], 
            #         [10 /image_size[0], 20 / image_size[1], 100 / image_size[0], 150 / image_size[1]]
            #         ],
            #     "labels": [0, 0],
            # }
            
            # # XYXY format
            # result_dict[img] = {
            #     "bboxes": [[0, 0, 200, 100], [10, 20, 110, 170]],
            #     "labels": [0, 0],
            # }
            
            # # REL_XYXY format
            result_dict[img] = {
                "bboxes": [
                    [0 / image_size[0], 0 / image_size[1], 200 / image_size[0], 100 / image_size[1]], 
                    [10 /image_size[0], 20 / image_size[1], 110 / image_size[0], 170 / image_size[1]]
                    ],
                "labels": [0, 0],
            }
        st.session_state["result"] = result_dict.copy()

    num_page = st.slider("page", 0, len(image_path_list) - 1, 1, key="slider_seg")
    target_image_path = image_path_list[num_page]
    
    with st.expander("Size & Label List"):
        c1, c2, = st.columns(2)
        with c1: _height = st.number_input("image_height (px)", min_value=0, value=512, key="image_height_seg")
        with c2: _width = st.number_input("image_width (px)", min_value=0, value=512, key="image_width_seg")
        
        _label_list = st.multiselect("Lable List", options=label_list, default=label_list, key="label_list_seg")
        
        c1, c2, c3 = st.columns(3)
        with c1: _ui_size = st.selectbox("ui_size", ("small", "medium", "large"), key="ui_size_seg")
    
        c1, c2, c3 = st.columns(3)
        with c1: _ui_left_size = st.selectbox("ui_left_size", (None, "small", "medium", "large", "custom"), key="ui_left_size_seg")
        if _ui_left_size == "custom":
            with c2: _ui_left_size = st.number_input("left_size (px)", min_value=0, value=198, key="left_size_seg")
        
        
        c1, c2, c3 = st.columns(3)
        with c1: _ui_bottom_size = st.selectbox("ui_bottom_size", (None, "small", "medium", "large", "custom"), key="ui_bottom_size_seg")
        if _ui_bottom_size == "custom":
            with c2: _ui_bottom_size = st.number_input("bottom_size (px)", min_value=0, value=198, key="bottom_size_seg")
            
        c1, c2, c3 = st.columns(3)
        with c1: _ui_right_size = st.selectbox("ui_right_size", (None, "small", "medium", "large", "custom"), key="ui_right_size_seg")
        if _ui_right_size == "custom":
            with c2: _ui_right_size = st.number_input("right_size (px)", min_value=0, value=34, key="right_size_seg")
    
    with st.expander("UI Setting & Position"):                
        c1, c2, c3 = st.columns(3)
        with c1: _ui_position = _item_editor_position = st.selectbox("ui_position", ("left", "right"), key="ui_position_seg")
        with c2: _line_width = st.number_input("line_width", min_value=0.5, value=1.0, step=0.1, key="line_width_seg")
    
    
        c1, c2, c3 = st.columns(3)
        with c1: _class_select_type = st.selectbox("class_select_type", ("select", "radio"), key="class_select_seg")
        with c2: _class_select_position = st.selectbox("class_select_position", (None, "left", "right", "bottom"), key="class_select_position_seg")
    
        c1, c2, c3 = st.columns(3)
        with c1: _item_editor = st.toggle("item_editor", True, "item_editor_seg")
        if _item_editor:
            with c2: _item_editor_position = st.selectbox("item_editor_position", (None, "left", "right"), key="item_editor_pos_seg")
            with c3: _edit_description = st.toggle("edit_description", key="edit_description_seg")
        else:
            _item_editor_position = None
            _edit_description = False
            
        c1, c2, c3 = st.columns(3)
        with c1: _item_selector = st.toggle("item_selector", True, key="item_selector_seg")
        if _item_selector:
            with c2: _item_selector_position = st.selectbox("item_selector_position", (None, "left", "right"), key="item_selector_pos_seg")
        else:
            _item_selector_position = None
    
    st.session_state.out = segmentation(
        image_path=target_image_path,
        bboxes=st.session_state["result"][target_image_path]["bboxes"],
        bbox_format="REL_XYXY",
        labels=st.session_state["result"][target_image_path]["labels"],
        label_list=_label_list,
        line_width=_line_width,
        class_select_type=_class_select_type,
        item_editor=_item_editor,
        item_selector=_item_selector,
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
    )
    st.session_state.out
    
    with st.expander("api"):
        st.code(f'''result = detection(
        image_path=image_path,
        label_list={_label_list},
        bboxes={st.session_state["result"][target_image_path]["bboxes"]},
        bbox_format='REL_XYXY'
        labels={st.session_state["result"][target_image_path]["labels"]},
        metaDatas=[],
        height={_height},
        width={_width},
        line_width={_line_width},
        ui_position={repr(_ui_position)},
        class_select_position={repr(_class_select_position)},
        item_editor_position={repr(_item_editor_position)},
        item_selector_position={repr(_item_selector_position)},
        class_select_type={repr(_class_select_type)},
        item_editor={_item_editor},
        item_selector={_item_selector},
        edit_description={_edit_description},
        ui_size={repr(_ui_position)},
        ui_left_size={repr(_ui_left_size)},
        ui_bottom_size={repr(_ui_bottom_size)},
        ui_right_size={repr(_ui_right_size)},
        key=None
    )''', language="python")