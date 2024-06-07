import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Slider from '@mui/material/Slider';
import MuiInput from '@mui/material/Input';
import { BaseComponentProps } from '../../utils/BaseComponent';

const Input = styled(MuiInput)`
  width: 42px;
`;

export interface InputSliderProps extends BaseComponentProps {
  minValue?: number;
  maxValue?: number;
  defaultValue?: number;
  title?: string;
  step?: number | null;
  value?: number;
  setValue?: (value: number) => void;
  disabled?: boolean;
}

export const InputSlider = ({
  width = "100%",
  height = "100%",
  minValue=0,
  maxValue=100,
  defaultValue=30,
  value=defaultValue,
  setValue,
  step,
  title="Select Value",
  disabled = false,
}: InputSliderProps) => {

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    if (setValue) {
      setValue(newValue as number);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    checkBoundary(event.target.value === '' ? 0 : Number(event.target.value));
  };

  const handleBlur = () => {
    checkBoundary(value);
  };
  
  const checkBoundary = (value: number) => {
    if (setValue) {
      if (value < minValue) {
        setValue(minValue);
      } else if (value > maxValue) {
        setValue(maxValue);
      } else {
        setValue(value);
      }
    }
  };

  return (
    <Box sx={{ width: width, height: height, p: "0px 6px"}}>
      <Grid container spacing={2} alignItems="center" lineHeight={1}>
        <Grid item xs>
          <Slider
            value={typeof value === 'number' ? value : 0}
            size={"small"}
            min={minValue}
            max={maxValue}
            onChange={handleSliderChange}
            aria-labelledby="input-slider"
            sx={{"padding":"15px 0px !important"}}
            disabled={disabled}
          />
        </Grid>
        <Grid item>
          <Input
            value={value}
            size="small"
            onChange={handleInputChange}
            onBlur={handleBlur}
            inputProps={{
              step: step,
              min: minValue,
              max: maxValue,
              type: 'number',
              'aria-labelledby': 'input-slider',
            }}
            disabled={disabled}
          />
        </Grid>
      </Grid>
    </Box>
  );
}