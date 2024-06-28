import {
  Streamlit,
} from "streamlit-component-lib"
import React, { useEffect, useState } from "react"
import { SelectChangeEvent } from '@mui/material/Select';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import useImage from 'use-image';
import { BBoxCanvas, ItemList, ClassSelect, ItemInfo, ClassRadio } from '../components';
import { BaseItem, Rectangle, PythonArgs } from '../utils'
import { CommmonArgs, DetectionArgs, DevArgs } from "../utils";

const _CLASS_SELECT_HEIGHT = 41 + 6;
const _SPACE = 8;

export const Detection = (args: PythonArgs) => {
  const {
    image_url,
    image_size,
    label_list = [],
    bbox_info = [],
    color_map = {},
    line_width = 1.0,
    class_select_type = "select",
    class_select_position = "right",
    item_editor = false,
    item_editor_position = "right",
    item_selector = false,
    item_selector_position = "right",
    ui_left_size = 0,
    ui_bottom_size = 0,
    ui_right_size = 0,
    edit_description = false,
    edit_meta = false,
    read_only = false,
    bbox_show_additional = false,
    bbox_show_label = false,
    justify_content = "start",
  }: CommmonArgs & DetectionArgs & DevArgs = args

  let left_width: number = 0;
  let left_height: number = 0;
  let right_width: number = 0;
  let right_height: number = 0;
  let bottom_height: number = 0;
  let left_item_num: number = 0;
  let right_item_num: number = 0;


  // Determine Size of Each Control UI Components
  switch (class_select_position) {
    case "left":
      left_width = ui_left_size;
      if (class_select_type === "radio") {
        left_item_num += 1;
      } else {
        left_height += _CLASS_SELECT_HEIGHT + _SPACE;
      }
      break;
    case "right":
      right_width = ui_right_size;
      if (class_select_type === "radio") {
        right_item_num += 1;
      } else {
        right_height += _CLASS_SELECT_HEIGHT + _SPACE;
      }
      break;
    case "bottom":
      bottom_height = class_select_type === "select" ? _CLASS_SELECT_HEIGHT + 4 : ui_bottom_size + _SPACE;

      break;
  }

  if (item_editor) {
    switch (item_editor_position) {
      case "left":
        left_width = ui_left_size;
        left_item_num += 1;
        break;
      case "right":
        right_width = ui_right_size;
        right_item_num += 1;
        break;
    }
  }

  if (item_selector) {
    switch (item_selector_position) {
      case "left":
        left_width = ui_left_size;
        left_item_num += 1;
        break;
      case "right":
        right_width = ui_right_size;
        right_item_num += 1;
        break;
    }
  }

  left_height = Math.trunc((window.innerHeight - left_height - _SPACE * Math.max(left_item_num - 1, 0)) / (left_item_num || 1));
  right_height = Math.trunc((window.innerHeight - right_height - _SPACE * Math.max(right_item_num - 1, 0)) / (right_item_num || 1));

  let radio_ui_height: number = ui_bottom_size;
  switch (class_select_position) {
    case "left":
      radio_ui_height = left_height;
      break;
    case "right":
      radio_ui_height = right_height;
      break;
    default:
      radio_ui_height = ui_bottom_size;
      break;
  }

  const params = new URLSearchParams(window.location.search);
  const baseUrl = params.get('streamlitUrl')
  const [image] = useImage(baseUrl + image_url)

  const [rectangles, setRectangles] = React.useState<Rectangle[]>(
    bbox_info.map((bb, i) => {
      return {
        x: bb.bbox[0],
        y: bb.bbox[1],
        width: bb.bbox[2],
        height: bb.bbox[3],
        label: bb.label,
        stroke: color_map[bb.label] || '#000',
        id: bb.id,
        meta: bb.meta || [],
        additional_data: bb.additional_data || {},
      }
    }));
  const [selectedId, setSelectedId] = React.useState<string | null>(null);
  const [label, setLabel] = useState<string>(label_list[0])
  const [mode, setMode] = React.useState<string>('Transform');
  const [selectedItem, setSelectedItem] = React.useState<Rectangle | null>(null);

  const [scale, setScale] = useState(1.0)
  useEffect(() => {
    const resizeCanvas = () => {
      const control_width = left_width + right_width;
      const scale_ratio = (window.innerWidth - control_width) / image_size[0];
      setScale(Math.min(scale_ratio, 1.0));
      Streamlit.setFrameHeight(image_size[1] * Math.min(scale_ratio, 1.0) + bottom_height);
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas()
  }, [image_size, left_width, right_width, bottom_height])

  const setStreamlitOutput = (rects: Rectangle[]) => {
    const currentBboxValue = rects.map((rect, i) => {
      return {
        bbox: [rect.x, rect.y, rect.width, rect.height],
        label_id: label_list.indexOf(rect.label),
        label: rect.label,
        id: rect.id,
        meta: rect.meta || [],
        additional_data: rect.additional_data || {},
      }
    })

    Streamlit.setComponentValue({
      "bbox": currentBboxValue,
      "key": Date.now().toString().slice(-8),
    })
  }

  const updateRectangle = (rects: {
    x: any;
    y: any;
    width: any;
    height: any;
    label: any;
    stroke: any;
    id: string;
    meta: string[];
  }[]) => {
    setRectangles(rects);

    if (selectedId !== null) {
      let index = rects.findIndex(rect => rect.id === selectedId);
      if (index !== -1) {
        setLabel(rects[index].label)
        setSelectedItem(rects[index])
      }
    }

    setStreamlitOutput(rects);
  };

  useEffect(() => {
    const newRectangles = bbox_info.map(bb => ({
      x: bb.bbox[0],
      y: bb.bbox[1],
      width: bb.bbox[2],
      height: bb.bbox[3],
      label: bb.label,
      stroke: color_map[bb.label] || '#000',
      id: bb.id,
      meta: bb.meta || [],
      additional_data: bb.additional_data || {},
    }));

    setRectangles(newRectangles);

    if (selectedId !== null) {
      let index = newRectangles.findIndex(rect => rect.id === selectedId);
      if (index !== -1) {
        setLabel(newRectangles[index].label)
        setSelectedItem(newRectangles[index])
      }
    }

    // setStreamlitOutput(newRectangles);
  }, [bbox_info, color_map]);

  const updateSelected = (selected: string | null) => {
    setSelectedId(selected)

    const rects = [...rectangles];
    let index = rects.findIndex(rect => rect.id === selected);
    if (selected && index !== -1) {
      setLabel(rects[index].label)
      setSelectedItem(rects[index])
    } else {
      setSelectedItem(null)
    }
  };

  const handleDelete = (id: string) => {
    const rects = [...rectangles];
    let index = rects.findIndex(rect => rect.id === id);
    if (index !== -1) {
      rects.splice(index, 1);
    }

    updateRectangle(rects);
    updateSelected(null);
    setStreamlitOutput(rects);
  };

  const handleClassSelectorChange = (event: SelectChangeEvent<string>) => {
    const value = event.target.value;

    setLabel(value)
    console.log(selectedId)
    if (!(selectedId === null)) {
      const rects = [...rectangles];
      let index = rects.findIndex(rect => rect.id === selectedId);
      if (index !== -1) {
        rects[index].label = value;
        rects[index].stroke = color_map[value];
      }
      updateRectangle(rects)
    }
  };

  const updateItem = (newItem: BaseItem) => {
    if (selectedId) {
      const rects = [...rectangles];
      let index = rects.findIndex(rect => rect.id === selectedId);
      if (index !== -1) {
        rects[index].id = newItem.id;
        rects[index].meta = newItem.meta;
      }
      setSelectedId(newItem.id);
      updateRectangle(rects);
    }
  };

  const ClassSelectRender = ({ marginTop, width = "calc(100%)" }: { marginTop?: number | string, width?: number | string }) => {
    return (
      class_select_type === "select" ?
        <ClassSelect
          width={width}
          height="calc(100%)"
          label={label}
          label_list={label_list}
          handleChange={handleClassSelectorChange}
          title="Current Class"
          marginTop={marginTop}
          disabled={read_only}
        /> :
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'start',
            flexWrap: 'wrap',
            listStyle: 'none',
            padding: '0px',
            width: width,
            maxHeight: `${radio_ui_height}px`,
            overflowY: "auto",
            overflowX: "clip",
            m: 0,
          }}
        >
          <ClassRadio
            vertical={class_select_position !== "bottom"}
            width="100%"
            height={radio_ui_height}
            label={label}
            label_list={label_list}
            handleChange={handleClassSelectorChange}
            multi={false}
            disabled={read_only}
          />
        </Box>
    );
  };

  const ElementEditorRender = ({ height }: { height: number }) => {
    return (
      <ItemInfo
        width="100%"
        height={`${height}px`}
        item={selectedId != null && selectedItem ? selectedItem : undefined}
        items={rectangles}
        edit={!read_only}
        displayLabel
        displayMetaData={edit_meta}
        displayDescription={!edit_meta && edit_description}
        setItem={updateItem}
      />
    );
  }

  const ElementSelectRender = ({ height }: { height: number }) => {
    return (
      <ItemList
        height={`${height}px`}
        items={rectangles}
        selectedId={selectedId}
        controlMode={read_only ? "none" : "delete"}
        colorMap={color_map}
        handleSecondary={handleDelete}
        handleSelect={updateSelected}
      />
    );
  }

  const RenderUi = ({ pos }: { pos: "left" | "right" }) => {
    let width: number = 0;
    let height: number = 0;

    switch (pos) {
      case "left":
        width = left_width;
        height = left_height;
        break;
      case "right":
        width = right_width;
        height = right_height;
        break;
    }

    return (
      <Stack
        direction="column"
        justifyContent="center"
        alignItems="center"
        spacing={`${_SPACE}px`}
        width={`${width}px`}
        sx={{ px: `${_SPACE}px` }}
      >
        {class_select_position === pos ? <ClassSelectRender /> : null}
        {(item_editor && item_editor_position === pos) ? <ElementEditorRender height={height} /> : null}
        {(item_selector && item_selector_position === pos) ? <ElementSelectRender height={height} /> : null}
      </Stack>
    );
  };

  return (
    <Box>
      <Stack
        direction="row"
        justifyContent={justify_content}
        alignItems="start"
      >

        {(left_width !== 0) ? <RenderUi pos={"left"} /> : undefined}

        <Stack
          direction="column"
          justifyContent="center"
          alignItems="center"
          spacing={`${_SPACE}px`}
          sx={{ px: "0px" }}
        >
          <BBoxCanvas
            rectangles={rectangles}
            mode={mode}
            selectedId={selectedId}
            scale={scale}
            setSelectedId={updateSelected}
            setRectangles={updateRectangle}
            setLabel={setLabel}
            color_map={color_map}
            label={label}
            image={image}
            image_size={image_size}
            strokeWidth={line_width}
            readOnly={read_only}
            showLabel={bbox_show_label}
            showAdditional={bbox_show_additional}
          />
          {class_select_position === "bottom" ? <ClassSelectRender marginTop={"10px !important"} width={image_size[0] * scale} /> : undefined}
        </Stack>

        {(right_width !== 0) ? <RenderUi pos={"right"} /> : undefined}
      </Stack>

    </Box>
  )
}
