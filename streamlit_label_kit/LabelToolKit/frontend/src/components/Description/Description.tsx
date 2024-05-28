import React, {useCallback, useEffect} from "react"

import { BaseComponentProps } from '../../utils/BaseComponent';
import IconButton from '@mui/material/IconButton';
import TextField from '@mui/material/TextField';
import SaveAsOutlinedIcon from '@mui/icons-material/SaveAsOutlined';
import ModeEditOutlineOutlinedIcon from '@mui/icons-material/ModeEditOutlineOutlined';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Input from '@mui/material/Input';
import InputBase from '@mui/material/InputBase';
import Paper from '@mui/material/Paper';


interface DescriptionProps extends BaseComponentProps {
  disabled?: boolean;
  description?: string;
  paddingLeft?: string | number;
  setDescription?: (value: string) => void;
}

let CONST_HEIGHT : number = 10;
let ROW_HEIGHT : number = 14;

export const Description = ({
  width = "100%",
  height = "auto",
  description = "",
  setDescription,
  disabled = false,
  paddingLeft = "0px",
}: DescriptionProps) => {

  const [tempValue, settempValue] = React.useState<string| null>(description);
  const [editable, setEditable] = React.useState(false);

  useEffect(() => {
    settempValue(description);
    setEditable(false);
  }, [description]);

  const renderInput = () => {
    return (

      <Stack
        direction="column"
        justifyContent="start"
        alignItems="center"
        spacing="4px"
        width={width}
        height={"100%"}
        sx={{ px: "0px" }}
      >
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          spacing="8px"
          width={width}
          
          sx={{ px: "0px", overflowY: "clip"}}
        >
          <Typography variant="body2" pl={paddingLeft}> {"Description: "}</Typography>
          <IconButton 
            size="small" 
            onClick={() => {
              setEditable(!editable);
              if (setDescription && editable) {
                setDescription(tempValue? tempValue : "");
              }
            }} 
            sx={{'& .MuiSvgIcon-root': { width: "1.2rem" }, padding: 0}}
            disabled={disabled}
            >
            {editable ? <SaveAsOutlinedIcon/> : <ModeEditOutlineOutlinedIcon/>}
          </IconButton>
        </Stack>
        {/* <Box sx={{ width, height: "calc(100% - 24px)", overflowY: "auto" }}> */}
        
        <Paper
          component="form"
          variant="outlined"
          sx={{
            borderRadius: "0.3rem",
            border: "1px solid rgba(0, 0, 0, 0.22)",
            p: '0',
            display: 'flex',
            alignItems: 'start',
            width: width,
            maxHeight: "calc(100% - 32px)",
            overflowY: "auto"
          }}
        >
          <InputBase
            id="outlined-multiline-static"
            value={tempValue}
            placeholder=""
            multiline={true}
            fullWidth
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                settempValue(event.target.value);
            }}
            disabled={disabled}
            readOnly={!editable}
            sx={{
              fontSize: "0.7rem", 
              p: 1, 
              '& .MuiInputBase-root': {
                p: 1, 
                fontSize: "0.8rem", 
                lineHeight: "1.5",
                alignItems: "start",
              },
              alignItems: "start",
            }}
          />
        </Paper>
      {/* </Box> */}
      </Stack>
    );
  }

  return (
    <Box sx={{ 
      width, 
      height:height, 
      // maxHeight:height, 
      overflowY: "clip", 
    }}>
      {renderInput()}
    </Box>
  );
};