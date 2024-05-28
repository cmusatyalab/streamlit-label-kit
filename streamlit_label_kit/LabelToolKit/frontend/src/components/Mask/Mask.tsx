import React, { useState } from 'react';
// import MaskCanvas from './MaskCanvas';
import { Select, MenuItem } from '@mui/material';

export interface MaskProps {
  image_url: string;
  label_list: string[];
  color_map: any;
}

export const Mask = ({ image_url, label_list, color_map }: MaskProps) => {
  const [label, setLabel] = useState(label_list[0]);
  const [masks, setMasks] = useState<any[]>([]);

  const handleLabelChange = (event: React.ChangeEvent<{ value: string }>) => {
    setLabel(event.target.value as string);
  };

  return (
    <div>
      <Select value={label}>
        {label_list.map((item, index) => (
          <MenuItem key={index} value={item}>{item}</MenuItem>
        ))}
      </Select>
      {/* <MaskCanvas image_url={image_url} scale={1} setMasks={setMasks} color_map={color_map} label={label} /> */}
      {/* Additional UI components to manage masks */}
    </div>
  );
};

export default Mask;
