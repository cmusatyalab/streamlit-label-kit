import React from "react"

import { BaseComponentProps } from '../../utils/BaseComponent';
import Paper from '@mui/material/Paper';

import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import ClearIcon from '@mui/icons-material/Clear';
import VisibilityOutlinedIcon from '@mui/icons-material/VisibilityOutlined';
import VisibilityOffOutlinedIcon from '@mui/icons-material/VisibilityOffOutlined';

import ListItemButton from '@mui/material/ListItemButton';
import IconButton from '@mui/material/IconButton';
import {BaseItem} from '../../utils'

interface ItemListProps extends BaseComponentProps {
  items: BaseItem[];
  selectedId?: string | null;
  disabledIds?: string[];
  colorMap?: {};
  controlMode?: "none" | "delete" | "visibility";
  handleSecondary?: (id: any) => void;
  handleSelect?: (id: any | null) => void;
} 

const getColor = (colorMap: any, label: string, defaultColor = "#FF0000") => {
  return colorMap[label] || defaultColor;
};

export const ItemList = ({
  width = "100%",
  height = "100%",
  items,
  selectedId,
  disabledIds = [],
  controlMode = "none",
  colorMap = {},
  handleSecondary,
  handleSelect,
}: ItemListProps) => {
  return (
    <Paper 
      variant="outlined" 
      sx={{
        width : width, 
        height : height,
        overflowY: "auto"
      }}>
      <List dense={true}>
        {items.map((item, index) =>

          <ListItem
            key={item.id}
            disabled={disabledIds.includes(item.id)}
            secondaryAction={ controlMode !== "none" ? (
              <IconButton 
                edge="end" 
                size="small"
                aria-label="secondary-action"
                sx={{'& .MuiSvgIcon-root': { width: "1.2rem" }}}
                onClick={handleSecondary ? () => handleSecondary(item.id) : undefined}
              >
                {controlMode === "delete" ? <ClearIcon /> : disabledIds.includes(item.id) ?  <VisibilityOffOutlinedIcon /> : <VisibilityOutlinedIcon />}
              </IconButton>) : undefined
            }
            sx={{"padding": 0}}
          >
            <ListItemButton
              selected={selectedId === item.id}
              key={item.id}
              onClick={handleSelect ? () => handleSelect(item.id) : undefined}
              dense
              sx={{pl: "8px"}}
            >
              <ListItemAvatar sx={{"minWidth": 28}}>
                <Avatar
                  sx={{ bgcolor: getColor(colorMap, item.label), width: 24, height: 24, fontSize: "1rem" }}
                >
                  {index + 1}
                </Avatar>
              </ListItemAvatar>
              
              <ListItemText primary={item.id} /> 
            </ListItemButton> 
          </ListItem>,
        )}
      </List>
    </Paper>
  );
};