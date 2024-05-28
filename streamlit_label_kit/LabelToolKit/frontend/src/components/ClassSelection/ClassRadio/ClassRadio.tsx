import React from "react"

import { ClassSelectorProps, SelectValue } from '../ClassSelectorComponent';
import { BaseComponentProps } from '../../../utils/BaseComponent';

import FormControl from '@mui/material/FormControl';
import Checkbox from '@mui/material/Checkbox';

import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';

/*
example of handelChange for multi

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
  };

example of handleChange for single

const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  setLabel(event.target.value)
};

*/
interface ClassRadioProps<Multiple extends boolean> extends BaseComponentProps, ClassSelectorProps<Multiple> {
  vertical?: boolean;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export const ClassRadio = <Multiple extends boolean = false>({
  vertical,
  width = "100%",
  height = "100%",
  label,
  label_list,
  handleChange,
  multi = false as Multiple
}: ClassRadioProps<Multiple>) => {
  return (
    <FormControl sx={{ width, height}} size="small">
      {multi ? (
        <FormGroup row={!vertical}>
          {label_list.map((name, index) => (
            <FormControlLabel
              key={index}
              control={
                <Checkbox
                  checked={label.indexOf(name) > -1}
                  onChange={handleChange}
                  name={name}
                  size="small"
                  sx={{ padding: "5px", paddingLeft: "12px" }}
                />
              }
              label={name}
              sx={{ mb: "0"}}
            />
          ))}
        </FormGroup>
      ) : (
        <RadioGroup
          row={!vertical}
          value={typeof label === 'string' ? label : ''}
          onChange={handleChange}
        >
          {label_list.map((name, index) => (
            <FormControlLabel
              key={index}
              value={name}
              control={<Radio size="small" sx={{ '& .MuiSvgIcon-root': { fontSize: 18 } }} />}
              label={name}
              sx={{
                m: 0,
                '& .MuiButtonBase-root': { padding: "5px", paddingLeft: "9px" },
              }}
            />
          ))}
        </RadioGroup>
      )}
    </FormControl>
  );
};