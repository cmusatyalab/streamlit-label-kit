// export interface PythonArgs {
//   image_url: string,
//   image_size: number[],
//   ui_width: number,
//   ui_height: number,
//   label_list?: string[],

//   bbox_info?: any[],
//   color_map?: any,
//   line_width?: number,
  
//   default_label_idx?: number,
//   vertical_layout?: boolean;
//   select_list?: boolean;
//   multi_select?: boolean;
//   default_multi_label_list?: string[];

//   label_type: "classification" | "detection" | "tag"
// }

export type PythonArgs = CommmonArgs & DetectionArgs & ClassificationArgs & DevArgs;

export interface CommmonArgs {
  image_url: string,
  image_size: number[],
  // ui_width?: number | string,
  // ui_height?: number,
  label_list?: string[],
  read_only?: boolean,
  label_type: "annotation" | "detection" | "segmentation"
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
  color_map?: any,
  line_width?: number,
  info_dict?: any[],
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