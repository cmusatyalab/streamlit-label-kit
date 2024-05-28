import React, { useCallback, useEffect } from "react"

import { BaseComponentProps } from '../../utils/BaseComponent';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import InputBase from '@mui/material/InputBase';
import AddOutlinedIcon from '@mui/icons-material/AddOutlined';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';

interface TagProps extends BaseComponentProps {
  disabled?: boolean;
  metaData?: string[];
  compact?: boolean;
  label?: string;
  setMetaData?: (value: string[]) => void;
}

export const Tag = ({
  width = "100%",
  height = "auto",
  metaData = [],
  compact = false,
  setMetaData,
  disabled = false,
  label = "tags",
}: TagProps) => {


  const [inputValue, setInputValue] = React.useState('');

  const handleDelete = useCallback((tag: string) => {
    const updatedMeta = metaData?.filter(t => t !== tag);
    if (setMetaData) {
      setMetaData(updatedMeta ? updatedMeta : []);
    }
  }, [metaData, setMetaData]);

  const handleAdd = useCallback(() => {
    if (!metaData?.includes(inputValue) && inputValue !== "") {
      let meta = [...metaData, inputValue];
      if (setMetaData) {
        setMetaData(meta);
      }
      setInputValue("");
    }
  }, [inputValue, metaData, setMetaData]);

  const handleKeyInteraction = useCallback((e: KeyboardEvent) => {
    if (e.type !== "keydown") {
      return;
    }

    if (e.key === "Enter") {
      handleAdd();
      e.preventDefault();
    }
  }, [handleAdd]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyInteraction);

    return () => {
      window.removeEventListener('keydown', handleKeyInteraction);
    };
  }, [handleKeyInteraction]);


  const renderInput = () => {
    return (
      <Paper
        component="form"
        variant="outlined"
        sx={{
          borderRadius: "1rem",
          border: "1px solid rgba(0, 0, 0, 0.22)",
          p: '0',
          display: 'flex',
          alignItems: 'center',
          width: width,
          height: "31.7px"
        }}
      >
        <InputBase
          sx={{ ml: 1, flex: 1, fontSize: "0.9rem" }}
          placeholder={disabled ? label : "add " + label}
          inputProps={{ 'aria-label': 'Add Meta Data' }}
          value={inputValue}
          onChange={(event) => {
            setInputValue(event.target.value);
          }}
          disabled={disabled}
        />

        {disabled ? null : <>
          <IconButton
            type="button"
            sx={{ p: '0', pr: '5px' }}
            aria-label="add-meta"
            onClick={handleAdd}
            disabled={disabled}
          >
            <AddOutlinedIcon />
          </IconButton>
        </>}
      </Paper>
    );
  }

  const renderChip = () => {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'start',
          flexWrap: 'wrap',
          listStyle: 'none',
          padding: '0px',
          width: "calc(100%)",
          maxHeight: "calc(100% - 34px)",
          overflowY: "auto",
          overflowX: "clip",
          m: 0,
        }}
      >

        {metaData.map((data, index) => (
          <Chip
            label={data}
            onDelete={disabled ? undefined : (() => handleDelete(data))}
            sx={{ m: "3px" }}
          />
        ))}
      </Box>
    );
  }

  const renderCompact = () => {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'start',
          flexWrap: 'wrap',
          listStyle: 'none',
          padding: '0px',
          width: width,
          maxHeight: "100%",
          overflowY: "auto",
          m: 0,
        }}
      >
        <Autocomplete
          multiple
          freeSolo
          size="small"
          id="tags-outlined"
          disabled={disabled}
          options={[]}
          value={metaData}
          getOptionLabel={(option) => option}
          filterSelectedOptions
          renderInput={(params) => (
            <TextField
              {...params}
              label={label}
              placeholder={"add " + label}
            />
          )}
          onChange={(event, newValue) => {
            if (setMetaData) {
              setMetaData(newValue)
            }
          }}
          sx={{ padding: "6px", width: "100%" }}
        />
      </Box>
    );
  }

  return (
    <Box sx={{ width, height:height, maxHeight:height, overflowY: "auto" }}>
      {compact ? renderCompact() : <>
        {renderInput()}
        {renderChip()}
      </>}
    </Box>
  );
};