import React from "react"

import { ClassSelectorProps, SelectValue } from '../ClassSelectorComponent';
import { BaseComponentProps } from '../../../utils/BaseComponent';

import InputLabel from '@mui/material/InputLabel';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';
import MenuItem from '@mui/material/MenuItem';
import Checkbox from '@mui/material/Checkbox';
import ListItemText from '@mui/material/ListItemText';

const ITEM_HEIGHT = 24;
const ITEM_PADDING_TOP = 6;
const MenuProps = {
  PaperProps: {
    style: {
      minHeight: ITEM_HEIGHT * 2.5 + ITEM_PADDING_TOP,
      width: 200,
      maxWidth: "100%"
    },
  },
};

interface ClassSelectProps<Multiple extends boolean> extends BaseComponentProps, ClassSelectorProps<Multiple> {
  title?: string;
  handleChange: (event: SelectChangeEvent<SelectValue<Multiple>>) => void;
  marginTop?: number | string;
}

export const ClassSelect = <Multiple extends boolean = false>({
  width = "100%",
  height = "100%",
  label,
  label_list,
  handleChange,
  multi = false as Multiple,
  title = multi ? "Select Classes" : "Select Class",
  marginTop = "6px !important",
  disabled = false,
}: ClassSelectProps<Multiple>) => {

  return (
    <FormControl sx={{ width: width, height: height, mt: marginTop}} size="small">
      <InputLabel id="classification-label">{title}</InputLabel>
      <Select
        labelId="classification-label"
        id={multi ? "classification-select-multiple" : "classification-select"}
        multiple={multi}
        value={label}
        onChange={handleChange}
        label={title}
        renderValue={multi ? (selected: any) => selected.join(', ') : undefined}
        MenuProps={MenuProps}
        disabled={disabled}
      >
        {label_list.map((option, index) => (
          <MenuItem key={index} value={option} sx={{ minHeight: "0px", py: "3px" }}>
            {multi && <Checkbox checked={Array.isArray(label) && label.includes(option)} size="small" sx={{ padding: "5px", paddingLeft: "5px" }} />}
            <ListItemText primary={option} sx={{ my: "0" }} />
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};
