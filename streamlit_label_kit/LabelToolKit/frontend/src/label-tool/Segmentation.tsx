import {
  Streamlit,
} from "streamlit-component-lib"
import React, { useEffect, useState } from "react"
import useImage from 'use-image';

import { SelectChangeEvent } from '@mui/material/Select';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import AddIcon from '@mui/icons-material/Add';
import SaveIcon from '@mui/icons-material/Save';
import EditIcon from '@mui/icons-material/Edit';

import { BBoxCanvas, ItemList, ClassSelect, ItemInfo, SegmentCanvas, InputSlider, BrushSelector, BrushEditor} from '../components';
import { BaseItem, Rectangle, PythonArgs, Mask} from '../utils'
import { CommmonArgs, SegmentationArgs, DevArgs } from "../utils";

const _CLASS_SELECT_HEIGHT = 42 + 6;
const _SPACE = 8;
const _SMALL_UI_WIDTH = 196;

const createEmptyMask = (width: number, height: number) => {
  return Array.from({ length: height }, () => Array<boolean>(width).fill(false));
}

export const Segmentation = (args: PythonArgs) => {
  const {
    image_url,
    image_size,
    label_list = [],
    masks_info = [],
    color_map = {},
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
    auto_seg_mode = false,
    read_only = false,
    justify_content = "start",
  }: CommmonArgs & SegmentationArgs & DevArgs = args

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
      bottom_height = class_select_type === "select" ?  _CLASS_SELECT_HEIGHT + 4 : ui_bottom_size + _SPACE;

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
  right_height = Math.trunc((window.innerHeight - right_height - _SPACE  * Math.max(right_item_num - 1, 0)) / (right_item_num || 1));

  const params = new URLSearchParams(window.location.search);
  const baseUrl = params.get('streamlitUrl')
  const [image] = useImage(baseUrl + image_url)

  const [selectedId, setSelectedId] = React.useState<string | null>(null);
  const [label, setLabel] = useState<string>(label_list[0])
  const [selectedItem, setSelectedItem] = React.useState<Mask | null>(null);
  const [editMode, setEditMode] = useState<"erase" | "pen">("pen")
  const [penShape, setPenShape] = useState<"circle" | "square">("circle");
  const [strokeSize, setStrokeSize] = useState(10);
  const [mode, setMode] = useState<"display" | "edit" | "new">("display");

  const [rectangles, setRectangles] = React.useState<Rectangle[]>([]);
  const [selectedRectId, setSelectedRectId] = React.useState<string | null>(null);

  const [masks, setMasks] = useState<Mask[]>(
    masks_info.map((mask, i) => {
    return {
      data: mask.data,
      width: image_size[0],
      height: image_size[1],
      label: mask.label,
      id: mask.id,
      meta: mask.meta || [],
      additional_data: mask.additional_data || {},
    }
  }));

  const [scale, setScale] = useState(1.0)
  useEffect(() => {
    const resizeCanvas = () => {
      const control_width = left_width + right_width;
      const scale_ratio = (window.innerWidth - control_width) / image_size[0];
      setScale(Math.min(scale_ratio, 1.0))
      Streamlit.setFrameHeight(image_size[1] * Math.min(scale_ratio, 1.0) + bottom_height + 1);
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas()
  }, [image_size, bottom_height, left_width, right_width])

  const setStreamlitOutput = (masks_input: Mask[] ) => {
    const currentMask = masks_input.map((mask, i) => {
      return {
        data: mask.data,
        width: mask.width,
        height: mask.height,
        label_id: label_list.indexOf(mask.label),
        label: mask.label,
        id: mask.id,
        meta: mask.meta || [],
        additional_data: mask.additional_data || {},
      }
    })

    const currentBboxValue = rectangles.map((rect, i) => {
      return {
        bbox: [rect.x, rect.y, rect.width, rect.height],
        label_id: label_list.indexOf(rect.label),
        label: rect.label,
        id: rect.id,
        meta: rect.meta || [],
        additional_data: rect.additional_data || {},
      }
    })

    setRectangles([]);

    Streamlit.setComponentValue({
      "new":  currentBboxValue,
      "mask": currentMask,
      "key": Date.now().toString().slice(-8),
    })
  }

  useEffect(() => {
    const newMasks = masks_info.map(mask => ({
        data: mask.data,
        width: image_size[0],
        height: image_size[1],
        label: mask.label,
        id: mask.id,
        meta: mask.meta || [],
        additional_data: mask.additional_data || {},
    }));
    setMasks(newMasks);

    if (selectedId !== null) {
      let index = newMasks.findIndex(rect => rect.id === selectedId);
      if (index !== -1) {
        setLabel(newMasks[index].label)
        setSelectedItem(newMasks[index])
      }
    } 

    setStreamlitOutput(newMasks);
  }, [masks_info]);

  const handleShapeChange = (value: string) => {
    if (value === "circle" || value === "square") {
      setPenShape(value)
    }
  };

  const handleEditModeChange = (value: string) => {
    if (value === "erase" || value === "pen") {
      setEditMode(value)
    }
  };

  const updateMasks = (masks: Mask[]) => {
    setMasks(masks);

    if (selectedId !== null) {
      let index = masks.findIndex(mask => mask.id === selectedId);
      if (index !== -1) {
        setLabel(masks[index].label)
        setSelectedItem(masks[index])
      }
    } 

    setStreamlitOutput(masks);
  };

  const updateSelected = (selected: string | null) => {
    setSelectedId(selected)

    const _masks = [...masks];
    let index = _masks.findIndex(mask => mask.id === selected);
    if (selected && index !== -1) {
      setLabel(_masks[index].label)
      setSelectedItem(_masks[index])
    } else {
      setSelectedItem(null)
    }
  };

  const handleDelete = (id: string) => {
    let _masks = [...masks];
    let index = _masks.findIndex(rect => rect.id === id);

    
    if (index !== -1) {
      if (_masks.length !== 1) {
        _masks.splice(index, 1)
      } else {
        _masks = []
      }
    }

    updateSelected(null);
    updateMasks(_masks);
  };

  const handleClassSelectorChange = (event: SelectChangeEvent<string>) => {
    const value = event.target.value;

    setLabel(value)
    console.log(selectedId)
    if (!(selectedId === null)) {
      const _masks = [...masks];
      let index = _masks.findIndex(mask => mask.id === selectedId);
      if (index !== -1) {
        _masks[index].label = value;
      }
      updateMasks(_masks)
    }
  };

  const updateItem = (newItem: BaseItem) => {
    if (selectedId) {
      const _masks = [...masks];
      let index = _masks.findIndex(mask => mask.id === selectedId);
      if (index !== -1) {
        _masks[index].id = newItem.id;
        _masks[index].meta = newItem.meta;
      }
      setSelectedId(newItem.id);
      updateMasks(_masks);
    }
  };


  const addNewMask = () => {
    const newMask = {
      data: createEmptyMask(image_size[0], image_size[1]),
      width: image_size[0],
      height: image_size[1],
      label: label,
      id: Date.now().toString().slice(-8),
      meta: [],
    };

    const newMasks = [...masks, newMask];
    setMasks(newMasks);
    updateSelected(newMask.id);
  }

  const removeOverlap = () => {
    const _masks = [...masks];
    if (selectedId) {
      let index = _masks.findIndex(mask => mask.id === selectedId);
      if (index !== -1) {
        const height = image_size[1];
        const width = image_size[0];

        for (let y = 0; y < height; y++) {
          for (let x = 0; x < width; x++) {
            if (masks[index].data[y][x]) {
              masks.map((mask) => { mask.data[y][x] = false;});
              masks[index].data[y][x] = true;
        }}}
      }  
    }
    updateMasks(_masks);
  }

  const updateMode = (e: any) => {
    if (mode === "display") {
      if (selectedId) {
        setMode("edit")
      } else {
        setMode("new");
        if (auto_seg_mode) {
          updateSelected(null);
        } else {
          addNewMask();
        }
      }
    } else {
      setMode("display");
      removeOverlap();
      updateSelected(null);
    }
  };

  const ClassSelectRender = ({ marginTop = "6px !important", width = "calc(100%)" }: { marginTop?: number | string , width?: number|string }) => {
    return (
      <Stack
        direction = "row"
        justifyContent="center"
        alignItems="center"
        minWidth={width}
        spacing={`${_SPACE}px`}
      >
        <IconButton
          sx={{"mt": marginTop, "border": "1px solid rgba(0, 0, 0, 0.12)", "border-radius": "4px"}}
          onClick={updateMode}
          disabled={read_only}
        >
          {
            mode === "display" ? (selectedId === null ? <AddIcon /> : <EditIcon />) : <SaveIcon />
          }
        </IconButton>
        <ClassSelect
          width="100%"
          height="calc(100%)"
          label={label}
          label_list={label_list}
          handleChange={handleClassSelectorChange}
          title="Current Class"
          marginTop={marginTop}
          disabled={read_only}
        />
      </Stack>
    );
  };

  const ElementEditorRender = ({ height }: { height: number }) => {
    return (
      <ItemInfo
        width="100%"
        height={`${height}px`}
        item={selectedId != null && selectedItem ? selectedItem : undefined}
        items={masks}
        edit = {!read_only && (mode === "display")}
        displayLabel
        displayMetaData = {edit_meta}
        displayDescription = {!edit_meta && edit_description}
        setItem={updateItem}
      />
    );
  }

  const ElementSelectRender = ({ height }: { height: number }) => {
    return (
      <ItemList
        height={`${height}px`}
        items={masks}
        selectedId={selectedId}
        controlMode={(!read_only && (mode === "display")) ? "delete" : "none"}
        colorMap={color_map}
        handleSecondary={handleDelete}
        handleSelect={(!read_only && (mode === "display")) ? updateSelected : undefined}
      />
    );
  }

  return (
    <Box>
      <Stack
        direction="row"
        justifyContent={justify_content}
        alignItems="start"
      >
        {(left_width !== 0) ?
          <Stack
            direction="column"
            justifyContent="center"
            alignItems="center"
            spacing={`${_SPACE}px`}
            width={`${left_width}px`}
            sx={{ px: `${_SPACE}px` }}
          >
            {class_select_position === "left" ? <ClassSelectRender /> : null}
            {
              (mode === "edit" || (mode === "new" && !auto_seg_mode) ) && (class_select_position === "left") ?
                <BrushEditor value={strokeSize} setValue={setStrokeSize} shape={penShape} setShape={handleShapeChange} mode={editMode} setMode={handleEditModeChange} disabled={read_only}/>:
                (mode === "display") || (class_select_position !== "left")? 
                  <Stack
                    direction="column"
                    justifyContent="center"
                    alignItems="center"
                    spacing={`${_SPACE}px`}
                    width={"100%"}
                  >
                    {(item_editor && item_editor_position === "left") ? <ElementEditorRender height={left_height} /> : null}
                    {(item_selector && item_selector_position === "left")? <ElementSelectRender height={left_height} /> : null}
                  </Stack> :
                  <Typography variant="body2"> Click and drag to draw a bounding box around the target object, then click save button </Typography>
            }
          </Stack> : undefined
        }
        
        <Stack
          direction="column"
          justifyContent="center"
          alignItems="center"
          spacing={`${_SPACE}px`}
          sx={{ px: "0px" }}
        >
          {(mode === "new" && auto_seg_mode) ? 
            <BBoxCanvas
              rectangles={rectangles}
              mode={'Transform'}
              selectedId={selectedRectId}
              scale={scale}
              setSelectedId={setSelectedRectId}
              setRectangles={setRectangles}
              setLabel={(e: any)=>{return}}
              color_map={color_map}
              label={label}
              image={image}
              image_size={image_size}
              strokeWidth={1}
            /> : 
            <SegmentCanvas
              image={image}
              image_size={image_size}
              scale={scale}
              masks={masks}
              setMasks={setMasks}
              selectedId={selectedId}
              setSelectedId={updateSelected}
              handleDelete={handleDelete}
              color_map={color_map}
              mode={mode}
              strokeShape={penShape}
              strokeSize={strokeSize}
              editMode={editMode}
            />
          }
          
          {class_select_position === "bottom" ? 
            <Stack
              direction="row"
              justifyContent="center"
              alignItems="center"
              spacing={`${_SPACE}px`}
              width={image_size[0] * scale}
            >
              <ClassSelectRender marginTop={"0px !important"} width={`calc(${_SMALL_UI_WIDTH}px)`}/> 
              {!auto_seg_mode ? <BrushSelector shape={penShape} setShape={handleShapeChange} mode={editMode} setMode={handleEditModeChange} disabled={mode==="display"}/> : <Typography variant="body2"> Click and drag to draw a bounding box around the target object, then click save button </Typography>}
              {!auto_seg_mode ? <InputSlider value={strokeSize} setValue={setStrokeSize} title={"Size"} minValue={1} maxValue={50} disabled={mode==="display"} /> : null}
            </Stack>
            : undefined}
        </Stack>

        {(right_width !== 0) ?
          <Stack
            direction="column"
            justifyContent="center"
            alignItems="center"
            spacing={`${_SPACE}px`}
            width={`${right_width}px`}
            sx={{ px: `${_SPACE}px` }}
          >
            {class_select_position === "right" ? <ClassSelectRender /> : null}
            {
              (mode === "edit" || (mode === "new" && !auto_seg_mode) ) && (class_select_position === "right") ?
                <BrushEditor value={strokeSize} setValue={setStrokeSize} shape={penShape} setShape={handleShapeChange} mode={editMode} setMode={handleEditModeChange} disabled={read_only}/>:
                (mode === "display") || (class_select_position !== "right")? 
                  <Stack
                    direction="column"
                    justifyContent="center"
                    alignItems="center"
                    spacing={`${_SPACE}px`}
                    width={"100%"}
                  >
                    {(item_editor && item_editor_position === "right") ? <ElementEditorRender height={right_height} /> : null}
                    {(item_selector && item_selector_position === "right")? <ElementSelectRender height={right_height} /> : null}
                  </Stack> :
                  <Typography variant="body2"> Click and drag to draw a bounding box around the target object, then click save button </Typography>
            }
          </Stack> : undefined
        }

      </Stack>
    </Box>
  )
}
