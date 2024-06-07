import * as React from 'react';
import BrushIcon from '@mui/icons-material/Brush';
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';
import StopIcon from '@mui/icons-material/Stop';
import Stack from '@mui/material/Stack';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import { BaseComponentProps } from '../../utils/BaseComponent';

interface BrushSelectorProps extends BaseComponentProps {
    shape?: string;
    setShape?: (value: string) => void;
    mode?: string;
    setMode?: (value: string) => void;
    disabled?: boolean;
  }

export function BrushSelector({
    shape = "circle",
    mode = "pen",
    setShape,
    setMode,
    width,
    disabled = false,
}: BrushSelectorProps) {

  const handleShapeChange = (
    event: React.MouseEvent<HTMLElement>,
    newAlignment: string,
  ) => {
    setShape && setShape(newAlignment);

  };

  const handleModeChange = (
    event: React.MouseEvent<HTMLElement>,
    newAlignment: string,
  ) => {
    setMode && setMode(newAlignment);
  };

  const penList = [
    <ToggleButton value="pen" key="pen">
      <BrushIcon />
    </ToggleButton>,
    <ToggleButton value="erase" key="erase">
      <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" viewBox="0 0 24 24"><path fill="currentColor" d="m16.24 3.56l4.95 4.94c.78.79.78 2.05 0 2.84L12 20.53a4.01 4.01 0 0 1-5.66 0L2.81 17c-.78-.79-.78-2.05 0-2.84l10.6-10.6c.79-.78 2.05-.78 2.83 0M4.22 15.58l3.54 3.53c.78.79 2.04.79 2.83 0l3.53-3.53l-4.95-4.95z"/></svg>
    </ToggleButton>,
  ];

  const shapeList = [
    <ToggleButton value="circle" key="circle">
      <FiberManualRecordIcon />
    </ToggleButton>,
    <ToggleButton value="square" key="square">
      <StopIcon />
    </ToggleButton>,
  ];

  const control_shape = {
    value: shape,
    onChange: handleShapeChange,
    exclusive: true,
  };

  const control_mode = {
    value: mode,
    onChange: handleModeChange,
    exclusive: true,
  };

  return (
    <Stack spacing={1} direction="row" alignItems="center" width={width}>
      <ToggleButtonGroup size="small" {...control_mode} aria-label="Small sizes" disabled={disabled}>
        {penList}
      </ToggleButtonGroup>
      <ToggleButtonGroup size="small" {...control_shape} aria-label="Small sizes" disabled={disabled}>
        {shapeList}
      </ToggleButtonGroup>
    </Stack>
  );
}