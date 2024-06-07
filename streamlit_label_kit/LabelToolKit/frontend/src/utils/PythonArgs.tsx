export type PythonArgs = CommmonArgs & DetectionArgs & ClassificationArgs & DevArgs;

export interface CommmonArgs {
  image_url: string,
  image_size: number[],
  label_list?: string[],
  read_only?: boolean,
  label_type: "annotation" | "detection" | "segmentation"
  justify_content?: "center" | "start" | "end"
};

export interface DevArgs {
  class_select_type?: "select" | "radio",
  class_select_position?: "right" | "left" | "bottom",
  item_editor?: boolean,
  item_editor_position?: "right" | "left",
  item_selector?: boolean,
  item_selector_position?: "right" | "left",
  ui_left_size?: number,
  ui_bottom_size?: number,
  ui_right_size?: number,
  edit_meta?: boolean,
  edit_description?: boolean,
};

export interface DetectionArgs {
  bbox_info?: any[],
  additional_bbox?: any[],
  color_map?: any,
  line_width?: number,
  bbox_show_additional?: boolean,
  bbox_show_label?: boolean,
}

export interface SegmentationArgs {
  masks_info?: any[],
  color_map?: any,
  auto_seg_mode?: boolean,
}

export interface ClassificationArgs {
  ui_width: number | string,
  ui_height: number,

  default_label_idx?: number,
  vertical_layout?: boolean,
  multi_select?: boolean,
  default_multi_label_list?: string[];

  class_select_type?: "select" | "radio",
  class_select_position?: "right" | "left" | "bottom",
  meta_editor?: boolean,
  meta_editor_position?: "right" | "left",
  
  ui_left_size?: number,
  ui_bottom_size?: number,
  ui_right_size?: number,

  meta_info?: any[],

  edit_class?: boolean,
  edit_meta?: boolean,
  edit_description?: boolean,
}