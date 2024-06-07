# Streamlit Label Kit

The Streamlit Label Kit is a comprehensive toolkit for building interactive image labeling and annotation UIs using Streamlit. It includes components for detection, classification, and segmentation, designed to facilitate easy integration into data processing workflows for machine learning and computer vision projects.

## Components Overview
- Detection: Allows users to define bounding boxes on images and label them according to a predefined set of categories.
- Annotation: Supports the classification of images or specific image features by selecting labels from a given list and editing metadata.
- Segmentation: Enables the creation and modification of image masks for pixel-level annotation.

## License

Unless otherwise stated, all source code and documentation are under the [GPL-2.0]. A copy of this license is included in the [LICENSE](LICENSE) file.

This project is inspired by and modified the content from following third-party sources:

| Project | Modified | License |
| --- | --- | --- |
| [hirune924/Streamlit-Image-Annotation](https://github.com/hirune924/Streamlit-Image-Annotation) | Yes | Apache-2.0 license |


## Install
```sh
pip install streamlit-label-kit
```

or

1. git clone this repo.
2. build frontend as following
```sh
cd streamlit_label_kit/LabelToolKit/frontend
yarn install
yarn build
```
3. activate your virtual environment
4. pip install -e .

## Example Uses
Checkout example/demo.py

run by 
```bash
pip install streamlit-label-kit

streamlit run --server.headless True --server.fileWatcherType none example/demo.py 
```

### Using the Demo
- Switch modes: Use the tabs at the top to switch between Detection, Classification, and Segmentation modes.
- Configure inputs: Use sliders and inputs to configure the component's behavior, like image size, UI size, and bbox format.
- Interact with UI: Directly interact with images to label them. Adjust settings in real-time to see how the component behaves.
- View outputs: Outputs are displayed below each component, showing the data structure returned by the component based on user interactions.
- Examples: See some more advanced use cases provided.


### Detection Overview
```python
from streamlit_label_kit import detection

# Example function call
result = detection(
    image_path="path/to/image.jpg",
    label_list=["dog", "cat"],
    bboxes=[[50, 50, 100, 100], [150, 150, 50, 50]],
    bbox_format="XYWH",
    line_width=1.0,
    ui_size="medium",
    read_only=False
)
```

### Annotation Overview
```python
from streamlit_label_kit import annotation

# Example function call
label = annotation(
    image_path="path/to/image.jpg",
    label_list=["happy", "sad"],
    label_index=0,
    classification=True,
    multi_select=False,
    ui_position="right"
)

```

### Segmentation Overview
```python
from streamlit_label_kit import segmentation

# Example function call
mask = segmentation(
    image_path="path/to/image.jpg",
    masks=[],
    label_list=["foreground", "background"],
    ui_size="large"
)
```

## API

### detection
```plaintext
detection(
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
)


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
```

### segmentation
```plaintext
segmentation(
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
)

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
```


### annotation
```plaintext
annotation(
    image_path (str, optional): Path to the image file. If not provided, no image is displayed.
    label_list (list[str], optional): List of available labels for classification.
    label_index (Union[int, list[int]], optional): Index or indices of the initially selected label(s) from `label_list`.
    image_height (int, optional): The height to which the image should be resized.
    image_width (int, optional): The width to which the image should be resized.
    classification (bool, optional): If True, enables the classification UI. Defaults to False.
    multi_select (bool, optional): Allows selection of multiple labels if True.
    ui_position (Literal["right", "left"], optional): Default position for UI controls.
    class_select_position (Literal["right", "left", "bottom"], optional): Position of the class selector UI.
    meta_editor_position (Literal["right", "left"], optional): Position of the metadata editor UI.
    class_select_type (Literal["select", "radio"], optional): Type of UI control for class selection.
    meta_editor (bool, optional): If True, enables metadata editing UI.
    edit_description (bool, optional): If True, enables an additional description field for metadata.
    meta_data (list[str], optional): List of metadata strings associated with the image.
    ui_size (Literal["small", "medium", "large"], optional): Base size for UI components.
    ui_left_size (Union[Literal, int], optional): Custom size for left-positioned UI elements.
    ui_bottom_size (Union[Literal, int], optional): Custom size for bottom-positioned UI elements.
    ui_right_size (Union[Literal, int], optional): Custom size for right-positioned UI elements.
    ui_bottom_fill_width (bool, optional): If True, the bottom UI fills the width of the viewport.
    ui_height (int, optional): Custom height for the UI components.
    read_only (bool, optional): If True, disables any interactions, making the UI read-only.
    component_alignment (Literal["left", "center", "right"], optional): Alignment of the UI components.
    key (any, optional): A unique key to differentiate this instance when using multiple components.
)

Output Format:
    {
        'label': str,   # Name of the selected label.
        'meta': [str],  # List of metadata strings associated with the annotation.
        'key': key,     # Unique identifier for the returned value.
    }
```