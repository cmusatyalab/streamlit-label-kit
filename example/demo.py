import streamlit as st
from glob import glob
import pandas as pd
from streamlit_label_kit import detection, classification

mode = st.tabs(["Detection", "Classification"])
label_list = ["deer", "human", "dog", "penguin", "framingo", "teddy bear"]
image_path_list = glob("image/*.jpg")

with mode[0]:
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

    new_labels = detection(
        image_path=target_image_path,
        bboxes=st.session_state["result_dict_det"][target_image_path]["bboxes"],
        labels=st.session_state["result_dict_det"][target_image_path]["labels"],
        label_list=label_list,
        key=target_image_path + "_det",
    )
    new_labels


with mode[1]: # Classification
    num_page = st.slider("page", 0, len(image_path_list) - 1, 1, key="slider_cls")

    c11, c12 = st.columns(2)
    with c11:
        "Default"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
        )
        label
    with c12:
        "Default - Three Labels"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list[:3],
            default_label_index=0,
        )
        label
        
    c21, c22 = st.columns(2)
    with c21:
        "Option: vertical"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            layout="vertical",
        )
        label
        
    with c22:
        "Option: vertical - Three Labels"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list[:3],
            default_label_index=0,
            layout="vertical",
        )
        label 
    
    c31, c32 = st.columns(2)
    with c31:
        "Option: multi"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            multi_select=True
        )
        label
    with c32:
        "Option: vertical, multi"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=[0, 2, 4],
            layout="vertical",
            multi_select=True
        )
        label
        
    c41, c42 = st.columns(2)
    with c41:
        "Option: select"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            select_list=True,
        )
        label      
    with c42:
        "Option: select, multi"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            select_list=True,
            multi_select=True
        )
        label
        

    c51, c52 = st.columns(2)
    with c51:
        "Option: vertical, select"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            layout="vertical",
            select_list=True,
        )
        label  
    with c52:  
        "Option: vertical, select, multi"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=[0, 2, 4],
            layout="vertical",
            select_list=True,
            multi_select=True
        )
        label
        
        
    c61, c62 = st.columns(2)
    with c61:
        "Option: vertical, large"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            layout="vertical",
            controller_size="large"
        )
        label
    with c62:
        "Option: large"
        label = classification(
            image_path=image_path_list[num_page],
            label_list=label_list,
            default_label_index=0,
            controller_size="large"
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

# with mode[3]:

#     if "result_df_cls" not in st.session_state:
#         st.session_state["result_df_cls"] = pd.DataFrame.from_dict(
#             {"image": image_path_list, "label": [0] * len(image_path_list)}
#         ).copy()

#     num_page = st.slider("page", 0, len(image_path_list) - 1, 0, key="slider_tag")

#     "default"
#     label = tag(
#         image_path_list[num_page],
#         label_list=label_list,
#         default_value=label_list,
#     )
#     label
    
#     "Option: large"
#     label = tag(
#         image_path_list[num_page],
#         label_list=label_list,
#         default_value=label_list + [str(num) for num in range(50)],
#         controller_size="large"
#     )
#     label
    
#     "Option: vertical"
#     label = tag(
#         image_path_list[num_page],
#         label_list=label_list,
#         default_value=label_list[:3],
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
     
   