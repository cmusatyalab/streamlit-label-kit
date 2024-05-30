import React, { useEffect } from "react";

import { BaseComponentProps } from '../../utils/BaseComponent';
import IconButton from '@mui/material/IconButton';
import SaveAsOutlinedIcon from '@mui/icons-material/SaveAsOutlined';
import ModeEditOutlineOutlinedIcon from '@mui/icons-material/ModeEditOutlineOutlined';

import Box from '@mui/material/Box';
import Input from '@mui/material/Input';
import Typography from '@mui/material/Typography';


interface ValueDisplayProps extends BaseComponentProps {
  label: string;
  value?: any;
  reservedValue?: string[];
  edit?: boolean;
  paddingLeft?: string | number;
  setValue?: (value: string) => void;
  disabled?: boolean,
} 

export const ValueDisplay = ({
  width = "100%",
  label,
  value = "",
  reservedValue = [],
  edit = false,
  paddingLeft = "0px",
  setValue,

}: ValueDisplayProps) => {
  const [tempValue, settempValue] = React.useState<string| null>(value);
  const [editable, setEditable] = React.useState(false);

  useEffect(() => {
    settempValue(value);
    setEditable(false);
  }, [value]);

  let selected = value !== "";
  let error = reservedValue.some(item => item === tempValue) && tempValue !== value;

  const renderEditIcon = () => {
    return ( 
      <IconButton 
        size="small" 
        onClick={() => {if (!error) {
          setEditable(!editable);
          if (setValue && editable) {
            setValue(tempValue? tempValue : value);
          }
        }}} 
        sx={{'& .MuiSvgIcon-root': { width: "1.2rem" }, padding: 0}}
        disabled={!selected}
        >
        {editable ? <SaveAsOutlinedIcon/> : <ModeEditOutlineOutlinedIcon/>}
      </IconButton>
    );
  }

  return (
    <Box
      sx={{ 
        p: '0', 
        display: 'flex', 
        alignItems: 'center', 
        width: width,
        height: "26px"
      }}
    >
      <Typography variant="body2" pl={paddingLeft}> {label + ": "}</Typography>
      <Input
        id="standard-size-normal"
        placeholder="Nothing Selected"
        value={tempValue}
        size={"small"}
        error={error}
        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            settempValue(event.target.value);
        }}
        readOnly={!editable}
        sx={{
          fontSize: "0.9rem", 
          pl: 0.5, 
          '& .MuiInputBase-input': {p: 0}
        }}
        disableUnderline={!editable}
      />
      {edit ? renderEditIcon(): null}
      
    </Box>
  );
};