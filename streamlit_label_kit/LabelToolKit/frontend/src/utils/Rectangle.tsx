import {BaseItem} from "./BaseItem"

export interface Rectangle extends BaseItem{
  x: number;
  y: number;
  width: number;
  height: number;
  stroke: any;
}