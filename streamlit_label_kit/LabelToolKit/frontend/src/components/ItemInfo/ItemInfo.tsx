import React, {useCallback} from "react"

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
import Box from '@mui/material/Box';
import {ValueDisplay} from '../ValueDisplay';
import {Tag} from '../Tag';


interface ItemInfoProps extends BaseComponentProps {
  item?: BaseItem;
  edit?: boolean;
  items?: BaseItem[];
  displayLabel?: boolean;
  displayMetaData?: boolean;
  setItem?: (item: BaseItem) => void;
} 

export const ItemInfo = ({
  width = "100%",
  height = "100%",
  item,
  items = [],
  displayLabel = false,
  displayMetaData = false,
  edit = false,
  setItem
}: ItemInfoProps) => {
  
  const updateId = useCallback((newId: string) => {
    if (setItem && item) {
      item.id = newId;
      setItem(item);
    }
  }, [setItem, item]);

  const updateMetaData = useCallback((newMeta: string[]) => {
    if (setItem && item) {
      item.meta = newMeta;
      setItem(item);
    }
  }, [setItem, item]);

  return (
    <Paper
      variant="outlined"
      sx={{
        width: width,
        height: height,
        overflowY: "clip",
        overflowX: "clip",
      }}
    >
      <Box
        sx={{
          display: 'block',
          justifyContent: 'start',
          listStyle: 'none',
          padding: '0px',
          width: "100%",
          height: "100%",
          p: "6px",
        }}
      >
        <ValueDisplay
          width="100%"
          label={"ID"}
          value={item?.id}
          reservedValue={items.map((it) => {return it.id;})}
          edit={edit}
          setValue={updateId}
          paddingLeft={"0.4rem"}
        />

        {displayLabel ? <> 
          <ValueDisplay
            width="100%"
            label={"label"}
            value={item?.label}
            paddingLeft={"0.4rem"}
          />
        </> : null}

        {displayMetaData ? <> 
          <Tag
            width="100%"
            height={`calc(100% - 24px - ${displayLabel ? '24px' : '0px'})`}
            label="Meta Data"
            disabled={(item === undefined) || !edit}
            metaData={item?.meta}
            setMetaData={updateMetaData}
          />
        </> : null}
      </Box>
    </Paper>
  );
};