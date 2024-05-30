import React, {useCallback} from "react"

import { BaseComponentProps } from '../../utils/BaseComponent';
import Paper from '@mui/material/Paper';
import {BaseItem} from '../../utils'
import Box from '@mui/material/Box';
import {ValueDisplay} from '../ValueDisplay';
import {Tag} from '../Tag';
import {Description} from '../Description'


interface ItemInfoProps extends BaseComponentProps {
  item?: BaseItem;
  edit?: boolean;
  items?: BaseItem[];
  displayLabel?: boolean;
  displayMetaData?: boolean;
  displayDescription?: boolean;
  additionalInfo?: {};
  setItem?: (item: BaseItem) => void;
} 

export const ItemInfo = ({
  width = "100%",
  height = "100%",
  item,
  items = [],
  displayLabel = false,
  displayMetaData = false,
  displayDescription = false,
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

  const updateDescription = useCallback((newDescription: string) => {
    if (setItem && item) {
      item.meta = [newDescription];
      setItem(item);
    }
  }, [setItem, item]);

  return (
    <Paper
      variant="outlined"
      sx={{
        width: width,
        height: height,
        // overflowY: "clip",
        overflowY: "auto",
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
            label={"Label"}
            value={item?.label}
            paddingLeft={"0.4rem"}
          />
        </> : null}

        {item?.additional_data ? Object.entries(item.additional_data).map(([title, info]) => (
          <ValueDisplay
            key={title}
            width="100%"
            label={title}
            value={info}
            paddingLeft={"0.4rem"}
          />
        )): null}

        {displayMetaData ? <> 
          <Tag
            width="100%"
            height={`calc(100% - 24px - ${displayLabel ? '24px' : '0px'})`}
            label="Meta Data"
            disabled={(item === undefined) || !edit}
            metaData={item?.meta}
            setMetaData={updateMetaData}
          />
        </> : displayDescription ? <> 
          <Description
            width="100%"
            height={`calc(100% - 24px - ${displayLabel ? '24px' : '0px'})`}
            disabled={(item === undefined) || !edit}
            description={item?.meta[0] || undefined}
            setDescription={updateDescription}
            paddingLeft={"0.4rem"}
          />
        </> : null}
      </Box>
    </Paper>
  );
};