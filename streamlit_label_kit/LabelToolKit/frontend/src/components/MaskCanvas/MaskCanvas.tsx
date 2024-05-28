import React, { useState, useEffect } from 'react';
import { Stage, Layer, Line, Image } from 'react-konva';
import useImage from 'use-image';

export interface MaskCanvasProps {
  image_url: string;
  scale: number;
  setMasks: (masks: any[]) => void;
  color_map: any;
  label: string;
}

export const MaskCanvas = ({ image_url, scale, setMasks, color_map, label }: MaskCanvasProps) => {
  const [drawing, setDrawing] = useState(false);
  const [masks, updateMasks] = useState<any[]>([]);
  const [image] = useImage(image_url);

  const handleMouseDown = (e: any) => {
    setDrawing(true);
    const pos = e.target.getStage().getPointerPosition();
    updateMasks([...masks, { tool: 'pen', points: [pos.x / scale, pos.y / scale], color: color_map[label] }]);
  };

  const handleMouseMove = (e: any) => {
    if (!drawing) return;
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    let lastMask = masks[masks.length - 1];
    lastMask.points = lastMask.points.concat([point.x / scale, point.y / scale]);
    masks.splice(masks.length - 1, 1, lastMask);
    updateMasks(masks.concat());
  };

  const handleMouseUp = () => {
    setDrawing(false);
    setMasks(masks);
  };

  return (
    <Stage width={window.innerWidth * scale} height={window.innerHeight * scale} onMouseDown={handleMouseDown} onMousemove={handleMouseMove} onMouseup={handleMouseUp}>
      <Layer>
        <Image image={image} width={window.innerWidth} height={window.innerHeight} />
        {masks.map((mask, i) => (
          <Line key={i} points={mask.points} stroke={mask.color} strokeWidth={5} tension={0.5} lineCap="round" lineJoin="round" />
        ))}
      </Layer>
    </Stage>
  );
};

export default MaskCanvas;
