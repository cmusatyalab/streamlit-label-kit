import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps
} from "streamlit-component-lib"
import React, { useEffect, useState, useCallback } from "react"
import { SelectChangeEvent } from '@mui/material/Select';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import useImage from 'use-image';
import { BBoxCanvas, ItemList, ClassSelect, ItemInfo } from '../components';
import { BaseItem, Rectangle, PythonArgs } from '../utils'

export const Detection = (args: PythonArgs) => {
  const {
    image_url,
    image_size,
    label_list = [],
    bbox_info = [],
    color_map = {},
    line_width = 1.0,
    ui_width,
    ui_height,
  }: PythonArgs = args

  const UI_WIDTH = ui_width;
  const UI_HEIGHT = ui_height;
  const left_control: boolean = false;
  const right_control: boolean = true;
  const bottom_control: boolean = false;

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
        stroke: color_map[bb.label],
        id: 'bbox-' + i,
        meta: [],
      }
    }));
  const [selectedId, setSelectedId] = React.useState<string | null>(null);
  const [label, setLabel] = useState<string>(label_list[0])
  const [mode, setMode] = React.useState<string>('Transform');
  const [selectedItem, setSelectedItem] = React.useState<Rectangle | null>(null);

  const [scale, setScale] = useState(1.0)
  useEffect(() => {
    const resizeCanvas = () => {
      const control_width = (left_control ? UI_WIDTH : 0) + (right_control ? UI_WIDTH : 0)
      const scale_ratio = (window.innerWidth - control_width) / image_size[0]
      setScale(Math.min(scale_ratio, 1.0))
      Streamlit.setFrameHeight(image_size[1] * Math.min(scale_ratio, 1.0) + (bottom_control ? UI_HEIGHT : 0))
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas()
  }, [image_size])

  const setStreamlitOutput = (rects: {
    x: any;
    y: any;
    width: any;
    height: any;
    label: any;
    stroke: any;
    id: string;
    meta: string[];
  }[],
    selected: string | null
  ) => {
    const currentBboxValue = rects.map((rect, i) => {
      return {
        bbox: [rect.x, rect.y, rect.width, rect.height],
        label_id: label_list.indexOf(rect.label),
        label: rect.label,
        meta: rect.meta
      }
    })
    let selectedRect = rects.filter((rct) => rct.id === selected)
    Streamlit.setComponentValue({
      "bbox": currentBboxValue,
      "selected": selectedRect.length === 0 ? null : selectedRect[0],
      "scale": scale
    })
  }

  const updateRectangle = useCallback((rects: {
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

    setStreamlitOutput(rects, selectedId);
  }, [selectedId, setRectangles, setLabel, setSelectedItem]);

  const handleClearAll = useCallback(() => {
    updateRectangle([])
  }, [updateRectangle]);


  const updateSelected = useCallback((selected: string | null) => {
    setSelectedId(selected)

    const rects = [...rectangles];
    let index = rects.findIndex(rect => rect.id === selected);
    if (index !== -1 && selected) {
      setLabel(rects[index].label)
      setSelectedItem(rects[index])
    } else {
      setSelectedItem(null)
    }
  
    setStreamlitOutput(rectangles, selected);

  }, [rectangles, setSelectedId, setStreamlitOutput, setSelectedItem]);

  const handleDelete = useCallback((id: string) => {
    const rects = [...rectangles];
    let index = rects.findIndex(rect => rect.id === id);
    if (index != -1) {
      rects.splice(index, 1);
    }

    updateRectangle(rects);
    updateSelected(null);
    setStreamlitOutput(rects, selectedId);
  }, [rectangles, selectedId, updateRectangle, updateSelected, setStreamlitOutput]);

  const handleClassSelectorChange = useCallback((event: SelectChangeEvent<string>) => {
    const value = event.target.value;

    setLabel(value)
    console.log(selectedId)
    if (!(selectedId === null)) {
      const rects = [...rectangles];
      let index = rects.findIndex(rect => rect.id === selectedId);
      if (index != -1) {
        rects[index].label = value;
        rects[index].stroke = color_map[value];
      }
      updateRectangle(rects)
    }
  }, [rectangles, selectedId, setLabel, updateRectangle]);

  const updateItem = useCallback((newItem: BaseItem) => {
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
  }, [setSelectedId, updateRectangle, rectangles, selectedId]);

  return (
    <Box>
      <Stack
        direction="row"
        justifyContent="center"
        alignItems="start"
        spacing={0.5}
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
        />

        <Stack
          direction="column"
          justifyContent="center"
          alignItems="center"
          spacing={"8px"}
          width={UI_WIDTH}
          sx={{ px: "8px" }}
        >
          <ClassSelect
            width={"calc(100%)"}
            height={"calc(100%)"}
            label={label}
            label_list={label_list}
            handleChange={handleClassSelectorChange}
            title={"Current Class"}
          />

          <ItemInfo
            width="100%"
            height="140px"
            item={selectedItem ? selectedItem : undefined}
            items={rectangles}
            edit
            displayLabel
            displayMetaData
            setItem={updateItem}
          />

          <ItemList
            height={window.innerHeight - 171 - UI_HEIGHT}
            items={rectangles}
            selectedId={selectedId}
            // disabledIds={rectangles.map((rct) => rct.id)}
            controlMode="delete"
            colorMap={color_map}
            handleSecondary={handleDelete}
            handleSelect={updateSelected}
          />

        </Stack>
      </Stack>
    </Box>
  )
}


// export default withStreamlitConnection(Classification)
