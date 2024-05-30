import React, { useState } from "react"
import { Rect, Text, Transformer } from 'react-konva';
import {Rectangle} from '../../utils/Rectangle';

export interface BBoxProps {
  rectProps: Rectangle,
  onChange: any,
  isSelected: boolean,
  fill: number,
  onClick: any,
  scale: number,
  strokeWidth: number
  showLabel?: boolean,
  showAddiontal?: boolean,
  readOnly?: boolean,
}

export const BBox = (props: BBoxProps) => {
  const shapeRef = React.useRef<any>();
  const trRef = React.useRef<any>();
  const {
    rectProps, onChange, isSelected, fill, onClick, scale, strokeWidth,
    showLabel = true,
    readOnly = false,
    showAddiontal = false,
  }: BBoxProps = props

  const [moving, setMoving] = useState(false);

  React.useEffect(() => {
    trRef.current?.nodes([shapeRef.current]);
    trRef.current?.getLayer().batchDraw();
  }, [isSelected]);

  function concatenateInfo(data: {}): string {
    const entries: string[] = [];

    Object.entries(data).forEach(([key, value]) => {
      let stringValue: string;
      if (value === null || value === undefined) {
      } else if (Array.isArray(value)) {
        stringValue = value.join(', ');
        entries.push(`${key}: ${stringValue}`);
      } else {
        stringValue = String(value);
        entries.push(`${key}: ${stringValue}`);
      }
    });

    return entries.join("\n");
  }
  

  return (
    <React.Fragment>
      {moving || showLabel && <Text text={rectProps.label} x={rectProps.x * scale + 5} y={rectProps.y * scale + 5} fontSize={15} fill={rectProps.stroke}/>}
      {(!moving && showAddiontal && rectProps.additional_data) ? <Text text={concatenateInfo(rectProps.additional_data)} x={rectProps.x * scale + 5} y={rectProps.y * scale + (showLabel ? 15 : 0) + 5} fontSize={15} fill={rectProps.stroke} />
        : null}
      <Rect
        onClick={onClick}
        ref={shapeRef}
        {...rectProps}
        stroke={''}
        x={rectProps.x * scale}
        y={rectProps.y * scale}
        width={rectProps.width * scale}
        height={rectProps.height * scale}
        draggable={isSelected && !readOnly}
        strokeWidth={isSelected ? strokeWidth + 1 : strokeWidth}
        fill={rectProps.stroke}
        opacity={fill}
        onDragStart={(e) => {
          setMoving(true)
        }}
        onDragEnd={(e) => {
          onChange({
            ...rectProps,
            x: e.target.x() / scale,
            y: e.target.y() / scale,
          });
          setMoving(false)
        }}
        onTransformStart={(e) => {
          setMoving(true)
        }}
        onTransformEnd={(e) => {
          // transformer is changing scale of the node
          // and NOT its width or height
          // but in the store we have only width and height
          // to match the data better we will reset scale on transform end
          const node = shapeRef.current;
          const scaleX = node.scaleX();
          const scaleY = node.scaleY();

          setMoving(false)

          // we will reset it back
          node.scaleX(1);
          node.scaleY(1);
          onChange({
            ...rectProps,
            x: node.x() / scale,
            y: node.y() / scale,
            // set minimal value
            width: Math.max(5, node.width() * scaleX / scale),
            height: Math.max(5, node.height() * scaleY / scale),
          });
        }}
      />

      <Transformer
        ref={trRef}
        resizeEnabled={isSelected && !readOnly}
        rotateEnabled={false}
        keepRatio={false}
        borderStroke={rectProps.stroke}
        borderStrokeWidth={isSelected && readOnly ? strokeWidth + 1 : strokeWidth}
        boundBoxFunc={(oldBox, newBox) => {
          // limit resize
          if (newBox.width < 5 || newBox.height < 5) {
            return oldBox;
          }
          return newBox;
        }}
      />

    </React.Fragment>
  );
};