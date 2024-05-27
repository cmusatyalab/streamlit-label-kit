import streamlit as st
from glob import glob
import pandas as pd
from streamlit_label_kit import detection, annotation

mode = st.tabs(["Detection", "Classification"])
label_list = ["deer", "human", "dog", "penguin", "framingo", "teddy bear"]
image_path_list = glob("image/*.jpg")



with mode[0]:
    
    title = st.text_input("Other Streamlit Component", "Life of Brian")
    st.write("Input Value is: ", title)
    
    if "result_dict_det" not in st.session_state:
        result_dict = {}
        for img in image_path_list:
            result_dict[img] = {
                "bboxes": [[0, 0, 200, 100], [10, 20, 100, 150]],
                "labels": [0, 1],
            }
        st.session_state["result_dict_det"] = result_dict.copy()

    num_page = st.slider("page", 0, len(image_path_list) - 1, 1, key="slider_det")
    target_image_path = image_path_list[num_page]
    

    with st.expander("detection api"):
        st.code('''def detection(
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
        meta_editor_position: Literal["right", "left"] = None,
        meta_selector_position: Literal["right", "left"] = None,

        class_select_type: Literal["select", "radio"] = "select",
        meta_editor: bool = True,
        meta_selector: bool = True,
        edit_description: bool = False,
        
        ui_size: Literal["small", "medium", "large"]= "small",
        ui_left_size: Union[Literal["small", "medium", "large"], int] = None,
        ui_bottom_size: Union[Literal["small", "medium", "large"], int] = None,
        ui_right_size: Union[Literal["small", "medium", "large"], int] = None,
        
        key=None,
            ) ''', language="python")


    st.session_state.new_value = detection(
        image_path=target_image_path,
        bboxes=st.session_state["result_dict_det"][target_image_path]["bboxes"],
        labels=st.session_state["result_dict_det"][target_image_path]["labels"],
        label_list=label_list,
        line_width=1.0,
        class_select_type="select",
        item_editor=True,
        item_selector=False,
        edit_description=True,
        # ui_position="bottom",
        class_select_position="left",
        item_editor_position="left",
        item_selector_position="left",
        height=512,
        width=512,
        ui_size="small",
        ui_left_size=None,
        ui_bottom_size=None,
        ui_right_size=None,
    )
    st.session_state.new_value

    
    

with mode[1]: # Classification
    num_page = st.slider("page", 0, len(image_path_list) - 1, 1, key="slider_cls")

    c11, c12 = st.columns(2)
    with c11:
        "Default"
        label = annotation(
            # image_path=image_path_list[num_page],
            classification=True,
            label_list=label_list,
            default_label_index=0,
        )
        label
    with c12:
        "Default - Three Labels"
        label = annotation(
            image_path=image_path_list[num_page],
            label_list=label_list[:3],
            classification=True,
            default_label_index=0,
        )
        label
        
    c21, c22 = st.columns(2)
    with c21:
        "Option: vertical"
        label = annotation(
            # image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            classification=True,
            class_select_position="bottom"
        )
        label
        
    with c22:
        "Option: vertical - Three Labels"
        label = annotation(
            # image_path=image_path_list[num_page],
            label_list=label_list[:3],
            default_label_index=0,
            classification=True,
            class_select_position="bottom"
        )
        label 
    
    c31, c32 = st.columns(2)
    with c31:
        "Option: multi"
        label = annotation(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            classification=True,
            multi_select=True
        )
        label
    with c32:
        "Option: vertical, multi"
        label = annotation(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=[0, 2, 4],
            classification=True,
            class_select_position="bottom",
            multi_select=True
        )
        label
        
    c41, c42 = st.columns(2)
    with c41:
        "Option: select"
        label = annotation(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            # select_list=True,
            classification=True,
            class_select_position="left",
            class_select_type="select",
        )
        label      
    with c42:
        "Option: select, multi"
        label = annotation(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            # select_list=True,
            classification=True,
            class_select_type="select",
            multi_select=True
        )
        label
        

    c51, c52 = st.columns(2)
    with c51:
        "Option: vertical, select"
        label = annotation(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            classification=True,
            class_select_position="bottom",
            class_select_type="select",
        )
        label  
    with c52:  
        "Option: vertical, select, multi"
        label = annotation(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=[0, 2, 4],
            classification=True,
            class_select_position="bottom",
            class_select_type="select",
            multi_select=True
        )
        label
        
        
    c61, c62 = st.columns(2)
    with c61:
        "Option: vertical, large"
        label = annotation(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            classification=True,
            class_select_position="bottom",
            ui_size="large"
        )
        label
    with c62:
        "Option: large"
        label = annotation(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            classification=True,
            ui_size="medium"
        )
        label
        
    "Option: item editor"
    label = annotation(
        image_path=image_path_list[num_page],
        label_list=label_list,
        default_label_index=0,
        classification=True,
        class_select_position="left",
        class_select_type="select",
        meta_editor=True,
        ui_height = 1000,
    )
    label  
    
    "Option: descriotion editor"
    label = annotation(
        # image_path=image_path_list[num_page],
        # label_list=label_list,
        default_label_index=0,
        classification=True,
        class_select_position="left",
        class_select_type="select",
        meta_editor=True,
        meta_editor_position ="left",
        ui_height = 200,
    )
    label  
    
    "Option: descriotion editor"
    label = annotation(
        # image_path=image_path_list[num_page],
        label_list=label_list,
        default_label_index=0,
        class_select_position="left",
        class_select_type="select",
        classification=False,
        meta_editor=True,
        meta_editor_position ="left",
        edit_description=True,
        ui_height = 200,
    )
    label  
# with mode[2]:

#     if "result_dict_point" not in st.session_state:
#         result_dict = {}
#         for img in image_path_list:
#             result_dict[img] = {
#                 "points": [[0, 0], [50, 150], [200, 200]],
#                 "labels": [0, 3, 4],
#             }
#         st.session_state["result_dict_point"] = result_dict.copy()

#     num_page = st.slider("page", 0, len(image_path_list) - 1, 0, key="slider_point")
#     target_image_path = image_path_list[num_page]

#     new_labels = pointdet(
#         image_path=target_image_path,
#         label_list=label_list,
#         points=st.session_state["result_dict_point"][target_image_path]["points"],
#         labels=st.session_state["result_dict_point"][target_image_path]["labels"],
#         key=target_image_path + "_point",
#     )
#     if new_labels is not None:
#         st.session_state["result_dict_point"][target_image_path]["points"] = [
#             v["point"] for v in new_labels
#         ]
#         st.session_state["result_dict_point"][target_image_path]["labels"] = [
#             v["label_id"] for v in new_labels
#         ]
#     st.json(st.session_state["result_dict_point"])

# with mode[2]:

#     if "result_df_cls" not in st.session_state:
#         st.session_state["result_df_cls"] = pd.DataFrame.from_dict(
#             {"image": image_path_list, "label": [0] * len(image_path_list)}
#         ).copy()

#     num_page = st.slider("page", 0, len(image_path_list) - 1, 0, key="slider_tag")

#     "default"
#     label = labelTag(
#         image_path_list[num_page],
#         label_list=label_list,
#         default_value=label_list,
#     )
#     label
    
#     "Option: large"
#     label = labelTag(
#         image_path_list[num_page],
#         label_list=label_list,
#         controller_size="large"
#     )
#     label
    
#     "Option: vertical"
#     label = labelTag(
#         image_path_list[num_page],
#         label_list=label_list,
#         layout="vertical",
#     )
#     label
    

#     "Option: vertical, large"
#     label = tag(
#         image_path_list[num_page],
#         label_list=label_list,
#         default_value=label_list + [str(num) for num in range(50)],
#         layout="vertical",
#         controller_size="large"
#     )
#     label

    
#     c1, c2 = st.columns(2)
#     with c1:
#         "Option: compact"
#         label = tag(
#             image_path_list[num_page],
#             label_list=label_list,
#             default_value=label_list[:3],
#             compact=True
#         )
#         label
#     with c2:
#         "Option: compact, vertical"
#         label = tag(
#             image_path_list[num_page],
#             label_list=label_list,
#             default_value=label_list[:2],
#             controller_size="small",
#             layout="vertical",
#             compact=True
#         )
#         label
     
   