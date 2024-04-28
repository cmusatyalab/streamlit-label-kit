import {
  Streamlit,
  ComponentProps
} from "streamlit-component-lib"
import React, { useEffect, useState } from "react"
import { SelectChangeEvent } from '@mui/material/Select';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import useImage from 'use-image';
import {ClassSelect, ClassRadio } from '../components';
import { PythonArgs } from '../utils'
import { Stage, Image, Layer } from 'react-konva';

export const Classification = ( args : PythonArgs) => {
  const {
    image_url,
    image_size,
    label_list = [],
    default_label_idx = 0,
    vertical_layout = false,
    select_list = false,
    multi_select = false,
    default_multi_label_list = [],
    ui_width,
    ui_height,
  }: PythonArgs = args

  const UI_WIDTH = ui_width;
  const UI_HEIGHT = ui_height;

  const params = new URLSearchParams(window.location.search);
  const baseUrl = params.get('streamlitUrl')
  const [image] = useImage(baseUrl + image_url)

  const [scale, setScale] = useState(1.0)
  const [label, setLabel] = useState(label_list[default_label_idx])
  const [labels, setLabels] = useState<string[]>(default_multi_label_list)

  const handleChangeCheckBox = (event: React.ChangeEvent<HTMLInputElement>) => {
    let result = [...labels];
    if (event.target.checked) {
      if (!result.includes(event.target.name)) {
        result.push(event.target.name);
      }
    } else {
      result = result.filter(i => i !== event.target.name);
    }
    setLabels(result)
    Streamlit.setComponentValue({ 'label': result })
  };

  const handleChange = (event: SelectChangeEvent) => {
    setLabel(event.target.value)
    Streamlit.setComponentValue({ 'label': event.target.value })
  };

  const handleChangeMulti = (event: SelectChangeEvent<typeof labels>) => {
    const {
      target: { value },
    } = event;
    const result = typeof value === 'string' ? value.split(',') : value;
    setLabels(result);
    Streamlit.setComponentValue({ 'label': result })
  };

  useEffect(() => {
    const resizeCanvas = vertical_layout ? () => {
      const scale_ratio = window.innerWidth / image_size[0]
      setScale(Math.min(scale_ratio, 1.0))
      Streamlit.setFrameHeight(image_size[1] * Math.min(scale_ratio, 1.0) + UI_HEIGHT)

    } : () => {
      const scale_ratio = (window.innerWidth - UI_WIDTH) / image_size[0]
      setScale(Math.min(scale_ratio, 1.0))
      Streamlit.setFrameHeight(image_size[1] * Math.min(scale_ratio, 1.0))
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas()
  }, [image_size])


  const window_height = vertical_layout ? (UI_HEIGHT) : window.innerHeight


  const renderSelectMultipleUI = () => {
    const width = vertical_layout ? window.innerWidth - 32 : UI_WIDTH - 32;
    return (
      <ClassSelect
        width={width} 
        height={"calc(100%-6px)"}
        label={labels}
        label_list={label_list}
        handleChange={handleChangeMulti}
        multi={true}
        />
    );
  }

  const renderSelectUI = () => {
    const width = vertical_layout ? window.innerWidth - 32 : UI_WIDTH - 32;
    return (
      <ClassSelect 
        width={width} 
        height={"calc(100%-6px)"} 
        label={label} 
        label_list={label_list} 
        handleChange={handleChange}
      />);
  }

  const renderRadioUI = () => {
    const width = vertical_layout ? "100%" : UI_WIDTH - 32;
    return (
      <ClassRadio
        vertical={vertical_layout}
        width="100%"
        height="auto"
        label={label}
        label_list={label_list}
        handleChange={handleChange}
        multi={false}
      />
    );
  }

  const renderCheckBoxUI = () => {
    const width = vertical_layout ? "100%" : UI_WIDTH - 32;
    return (
    <ClassRadio
        vertical={vertical_layout}
        width="100%"
        height="auto"
        label={labels}
        label_list={label_list}
        handleChange={handleChangeCheckBox}
        multi={true}
      />);
  }

  return (
    <Box>
      <Stack
        direction={vertical_layout ? "column" : "row"}
        justifyContent="center"
        alignItems={vertical_layout ? "center" : "start"}
        spacing={vertical_layout ? 0.5 : 1}
      >
        <Stage width={image_size[0] * scale} height={image_size[1] * scale}>
          <Layer>
            <Image image={image} scaleX={scale} scaleY={scale} />
          </Layer>
        </Stage>

        <Box sx={{
          overflowY: "auto",
          overflowX: "clip",
          height: window_height,
          m: "0px"
        }}>
          {select_list ? (multi_select ? renderSelectMultipleUI() : renderSelectUI()) : (multi_select ? renderCheckBoxUI() : renderRadioUI())}
        </Box>

      </Stack>
    </Box>
  );

}