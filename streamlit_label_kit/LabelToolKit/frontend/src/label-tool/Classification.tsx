import {
  Streamlit,
  ComponentProps
} from "streamlit-component-lib"
import React, { useEffect, useState, useCallback } from "react"
import { SelectChangeEvent } from '@mui/material/Select';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import useImage from 'use-image';
import {ClassSelect, ClassRadio, Tag, Description } from '../components';
import { PythonArgs } from '../utils'
import { CommmonArgs, ClassificationArgs } from "../utils";
import { Stage, Image, Layer } from 'react-konva';

const _CLASS_SELECT_HEIGHT = 41 + 6;
const _SPACE = 8;

export const Classification = ( args : PythonArgs) => {
  const {
    image_url,
    image_size,
    label_list = [],
    default_label_idx = 0,
    multi_select = false,
    default_multi_label_list = [],
    class_select_type = "select",
    class_select_position = "right",
    meta_editor = false,
    meta_editor_position = "right",
    ui_left_size = 0,
    ui_bottom_size = 0,
    ui_right_size = 0,
    meta_info = [],
    edit_class = true,
    edit_meta = false,
    edit_description = false,
    ui_width = "100%",
    ui_height,
  }: CommmonArgs & ClassificationArgs = args

  let left_width: number = 0;
  let left_height: number = 0;
  let right_width: number = 0;
  let right_height: number = 0;
  let bottom_height: number = 0;
  let left_meta_num: number = 0;
  let right_meta_num: number = 0;

  if (edit_class) {
    switch (class_select_position) {
      case "left":
        left_width = ui_left_size;
        if (class_select_type == "radio") {
          left_meta_num += 1;
        } else {
          left_height += _CLASS_SELECT_HEIGHT + _SPACE;
        }  
        break;
      case "right":
        right_width = ui_right_size;
        if (class_select_type == "radio") {
          right_meta_num += 1;
        } else {
          right_height += _CLASS_SELECT_HEIGHT + _SPACE;
        }
        break;
      case "bottom":
        bottom_height = class_select_type === "select" ?  _CLASS_SELECT_HEIGHT + 4: ui_bottom_size + _SPACE;
        break;
    }
  }
  
  if (meta_editor) {
    switch (meta_editor_position) {
      case "left":
        left_width = ui_left_size;
        left_meta_num += 1;
        break;
      case "right":
        right_width = ui_right_size;
        right_meta_num += 1;
        break;
    }
  }

  const UI_HEIGHT = image_size[0] === 0 ? ui_height : window.innerHeight;
  const UI_WIDTH = ui_width;

  left_height = Math.trunc((UI_HEIGHT - left_height - _SPACE * Math.max(left_meta_num - 1, 0)) / (left_meta_num || 1));
  right_height = Math.trunc((UI_HEIGHT- right_height - _SPACE  * Math.max(right_meta_num - 1, 0)) / (right_meta_num || 1));
  
  let radio_ui_height: number = ui_bottom_size;
  switch (class_select_position) {
    case "left":
      radio_ui_height = left_height;
      break;
    case "right":
      radio_ui_height = right_height;
      break;
    default:
      radio_ui_height = image_size[0] === 0 ? Math.max(ui_bottom_size, UI_HEIGHT) : ui_bottom_size;
      radio_ui_height = ui_bottom_size;
      break;
  }

  const params = new URLSearchParams(window.location.search);
  const baseUrl = params.get('streamlitUrl')
  const [image] = useImage(baseUrl + image_url)
  const [scale, setScale] = useState(1.0)
  const [label, setLabel] = useState<string>(label_list.length !== 0 ? label_list[default_label_idx] : "")
  const [labels, setLabels] = useState<string[]>(default_multi_label_list)
  const [meta, setMeta] = useState<string[]>(meta_info)


  const updateMeta = useCallback((newMeta: string[]) => {
    setMeta(newMeta)
    Streamlit.setComponentValue({ 'label': multi_select ? labels : label, 'meta': newMeta })
  }, [meta, setMeta]);

  const updateDescription = useCallback((newDescription: string) => {
    setMeta([newDescription])
    Streamlit.setComponentValue({ 'label': multi_select ? labels : label, 'meta': [newDescription] })
  }, [meta, setMeta]);

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
    Streamlit.setComponentValue({ 'label': result, 'meta': meta  })
  };

  const handleChange = (event: SelectChangeEvent<string | string[]>) => {
    const value = event.target.value;
    setLabel(typeof value === 'string' ? value : value.join(', '));
    Streamlit.setComponentValue({ 'label': value, 'meta': meta });
  };
  
  const handleChangeMulti = (event: SelectChangeEvent<string | string[]>) => {
    const value = event.target.value;
    const result = typeof value === 'string' ? value.split(',') : value;
    setLabels(result);
    Streamlit.setComponentValue({ 'label': result, 'meta': meta });
  };


  useEffect(() => {
    const resizeCanvas = () => {
      if (image_size[0] === 0) {
        Streamlit.setFrameHeight(UI_HEIGHT);
      } else {
        const control_width = left_width + right_width;
        const scale_ratio = (window.innerWidth - control_width) / image_size[0];
        setScale(Math.min(scale_ratio, 1.0))
        Streamlit.setFrameHeight(image_size[1] * Math.min(scale_ratio, 1.0) + bottom_height);
      }
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas()
  }, [image_size])

  let buttom_ui_width: number | string = image_size[0] !== 0 ? image_size[0] * scale : UI_WIDTH;

  const ElementEditorRender = ({ height }: { height: number }) => {
    return (
      <> 
        {edit_meta && ( 
          <Tag
            width="100%"
            height={`${height}px`}
            label="Meta Data"
            disabled={false} 
            metaData={meta}
            setMetaData={updateMeta}
          />
        )}
  
        {!edit_meta && edit_description && (
          <Description
            width="100%"
            height={`${height}px`}
            disabled={false} 
            description={meta[0]} 
            setDescription={updateDescription}
            paddingLeft={"0.4rem"}
          />
        )}
      </>
    );
  }

  const ClassSelectRender = ({ marginTop, multi, width = "calc(100%)"}: { marginTop?: number | string, multi: boolean, width?: number|string}) => {
    return (
      class_select_type === "select" ? 
        <ClassSelect
            width={width}
            height="auto"
            label={multi ? labels : label}
            label_list={label_list}
            handleChange={multi ? handleChangeMulti : handleChange}
            marginTop={marginTop}
            multi={multi}
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
              label={multi ? labels : label}
              label_list={label_list}
              handleChange={multi ? handleChangeCheckBox : handleChange}
              multi={multi}
          />
        </Box>
    );
  };


  const RenderUi = ({pos} : {pos: "left" | "right"}) => {
    let width: number = 0;
    let height: number = 0;

    switch(pos) {
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
        justifyContent="start"
        alignItems="center"
        spacing={`${_SPACE}px`}
        width={`${width}px`}
        height={window.innerHeight}
        sx={{ px: `${_SPACE}px`}}
      >
        {(edit_class && class_select_position === pos) ? <ClassSelectRender multi={multi_select} /> : null}
        {(meta_editor && meta_editor_position === pos) ? <ElementEditorRender height={height} /> : null}
      </Stack>
    );
  }

  return (
    <Box>
      <Stack
        direction="row"
        justifyContent="center"
        alignItems="start"
      >
        {left_width !== 0 ? <RenderUi pos={"left"}/> : null}

        <Stack
          direction="column"
          justifyContent="center"
          alignItems="center"
          spacing={`${_SPACE}px`}
          sx={{ px: "0px" }}
        >
          <Stage width={image_size[0] * scale} height={image_size[1] * scale}>
            <Layer>
              <Image image={image} scaleX={scale} scaleY={scale} />
            </Layer>
          </Stage>
          {(edit_class && class_select_position === "bottom") ? <ClassSelectRender multi={multi_select} marginTop={"10px !important"} width={buttom_ui_width} /> : undefined}
        </Stack>

        {(right_width !== 0) ? <RenderUi pos={"right"}/> : null}
      </Stack>
    </Box>
  );

}