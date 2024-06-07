import {BaseItem} from "./BaseItem"

export interface Mask extends BaseItem{
  data: boolean[][];
  width: number;
  height: number;
}