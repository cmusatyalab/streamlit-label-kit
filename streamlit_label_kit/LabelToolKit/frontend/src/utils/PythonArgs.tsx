export interface PythonArgs {
  image_url: string,
  image_size: number[],
  ui_width: number,
  ui_height: number,
  label_list?: string[],

  bbox_info?: any[],
  color_map?: any,
  line_width?: number,
  
  default_label_idx?: number,
  vertical_layout?: boolean;
  select_list?: boolean;
  multi_select?: boolean;
  default_multi_label_list?: string[];

  label_type: "classification" | "detection" | "tag"
}