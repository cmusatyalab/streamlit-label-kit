import * as React from 'react';
import Stack from '@mui/material/Stack';
import { BaseComponentProps } from '../../utils/BaseComponent';
import {InputSlider} from '../InputSlider';
import {BrushSelector} from '../BrushSelector'

import Paper from '@mui/material/Paper';


interface BrushEditorProps extends BaseComponentProps {
    shape?: string;
    setShape?: (value: string) => void;
    mode?: string;
    setMode?: (value: string) => void;
    value?: number;
    setValue?: (value: any) => void;
    disabled?: boolean;
  }

export function BrushEditor({
    shape = "circle",
    mode = "pen",
    value = 0,
    setValue,
    setShape,
    setMode,
    width = "100%",
    disabled = false,
}: BrushEditorProps) {

  return (
    <Paper
        variant="outlined"
        sx={{
          width: width,
          overflowY: "auto",
          overflowX: "clip",
        }}
      >
        <Stack
          direction="column"
          justifyContent="center"
          alignItems="center"
          spacing={`${6}px`}
          width={`100%`}
          p={"6px"}
        >
          <BrushSelector shape={shape} setShape={setShape} mode={mode} setMode={setMode} disabled={disabled}/>
          <InputSlider value={value} setValue={setValue} title={"Size"} minValue={1} maxValue={50} disabled={disabled}/>
        </Stack>
      </Paper>
  );
}