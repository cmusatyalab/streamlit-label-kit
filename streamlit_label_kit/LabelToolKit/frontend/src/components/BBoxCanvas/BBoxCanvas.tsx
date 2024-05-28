import React, { useState, useEffect, useCallback } from "react"
import { Layer, Rect, Stage, Image } from 'react-konva';
import {BBox} from '../BBox'
import Konva from 'konva';
import { Container } from "konva/lib/Container";

export interface BBoxCanvasLayerProps {
  rectangles: any[],
  mode: string,
  selectedId: string | null,
  setSelectedId: any,
  setRectangles: any,
  setLabel: any,
  color_map: any,
  scale: number,
  label: string,
  image_size: number[],
  image: any,
  strokeWidth: number
}

const MIN_SIZE = 5;
const MOVE_PIXEL = 5;
const KEY_NAMES = new Set<string>([
  "ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Delete", "Escape",
])

let keyState: { [key: string]: boolean } = {}

export const BBoxCanvas = (props: BBoxCanvasLayerProps) => {
  const {
    rectangles,
    mode,
    selectedId,
    setSelectedId,
    setRectangles,
    setLabel,
    color_map,
    scale,
    label,
    image_size,
    image,
    strokeWidth
  }: BBoxCanvasLayerProps = props
  const [adding, setAdding] = useState<number[] | null>(null)
  
  const handleDeselect = useCallback((e: Konva.KonvaEventObject<MouseEvent>) => {
    if (!(e.target instanceof Konva.Rect)) {
      setSelectedId(null);
      if (mode === 'Transform') {
        const pointer = e.target.getStage()?.getPointerPosition();
        if (pointer) {
          setAdding([pointer.x, pointer.y, pointer.x, pointer.y]);
        }
      }
    }
  }, [mode, setSelectedId, setAdding]);

  const handleKeyInteraction = useCallback((e: KeyboardEvent) => {
    if (e.type !== "keydown") {
      return
    }
    
    if (!KEY_NAMES.has(e.key) || selectedId === null) return;

    let updated = true

    if (updated) {
      let rects = [...rectangles];
      let index = rects.findIndex(rect => rect.id === selectedId);
      if (index === -1) return;

      switch (e.key) {
        case "Delete":
          rects = rects.filter((_, idx) => idx !== index);
          setSelectedId(null);
          break;
        case "Escape":
          setSelectedId(null);
          break;
        case "ArrowRight":
          rects[index].x += MOVE_PIXEL / scale;
          break;
        case "ArrowLeft":
          rects[index].x -= MOVE_PIXEL / scale;
          break;
        case "ArrowUp":
          rects[index].y -= MOVE_PIXEL / scale;
          break;
        case "ArrowDown":
          rects[index].y += MOVE_PIXEL / scale;
          break;
      }

      setRectangles(rects);
    }
    e.preventDefault();
  }, [rectangles, selectedId, setRectangles, setSelectedId, scale]);

  useEffect(() => {
    const rects = rectangles.slice();
    for (let i = 0; i < rects.length; i++) {
      if (rects[i].width < 0) {
        rects[i].width = rects[i].width * -1
        rects[i].x = rects[i].x - rects[i].width
        setRectangles(rects)
      }
      if (rects[i].height < 0) {
        rects[i].height = rects[i].height * -1
        rects[i].y = rects[i].y - rects[i].height
        setRectangles(rects)
      }
      if (rects[i].x < 0 || rects[i].y < 0) {
        rects[i].width = rects[i].width + Math.min(0, rects[i].x)
        rects[i].x = Math.max(0, rects[i].x)
        rects[i].height = rects[i].height + Math.min(0, rects[i].y)
        rects[i].y = Math.max(0, rects[i].y)
        setRectangles(rects)
      }
      if (rects[i].x + rects[i].width > image_size[0] || rects[i].y + rects[i].height > image_size[1]) {
        rects[i].width = Math.min(rects[i].width, image_size[0] - rects[i].x)
        rects[i].height = Math.min(rects[i].height, image_size[1] - rects[i].y)
        setRectangles(rects)
      }
      if (rects[i].width < MIN_SIZE || rects[i].height < MIN_SIZE) {
        rects[i].width = MIN_SIZE
        rects[i].height = MIN_SIZE
      }
    }

    window.addEventListener('keydown', handleKeyInteraction);
    window.addEventListener('keyup', handleKeyInteraction);

    return () => {
      window.removeEventListener('keydown', handleKeyInteraction);
      window.removeEventListener('keyup', handleKeyInteraction);
    };
  }, [rectangles, image_size, selectedId, handleKeyInteraction])

  return (
    <Stage 
      width={image_size[0] * scale} 
      height={image_size[1] * scale}
      onMouseDown={handleDeselect}
      onMouseMove={(e: any) => {
        if (adding) {
          const pointer = e.target.getStage()?.getPointerPosition()
          if (pointer){
            setAdding([adding[0], adding[1], pointer.x, pointer.y])
          }
        }
      }}
      onMouseLeave={(e: any) => {
        setAdding(null)
      }}
      onMouseUp={(e: any) => {
        if (adding && Math.abs((adding[2] - adding[0]) / scale) >= MIN_SIZE && Math.abs((adding[3] - adding[1]) / scale) >= MIN_SIZE) {
          const newRect = {
            x: adding[0] / scale,
            y: adding[1] / scale,
            width: (adding[2] - adding[0]) / scale,
            height: (adding[3] - adding[1]) / scale,
            label,
            id: Date.now().toString().slice(-8),
            stroke: color_map[label],
            meta: []
          };
          setRectangles([...rectangles, newRect]);
          setSelectedId(newRect.id);
        }
        setAdding(null);
      }}
      >
        
      <Layer>
        <Image image={image} scaleX={scale} scaleY={scale} />
      </Layer>
      <Layer>
        {rectangles.map((rect, i) => {
          return (
            <BBox
              key={i}
              rectProps={rect}
              scale={scale}
              fill={0.3}
              strokeWidth={strokeWidth}
              isSelected={mode === 'Transform' && rect.id === selectedId}
              onClick={() => {
                if (mode === 'Transform') {
                  setSelectedId(rect.id); 
                  setLabel(rect.label)
                } else if (mode === 'Del') {
                  const rects = rectangles.slice();
                  setRectangles(rects.filter((element) => element.id !== rect.id));
                }
              }}
              onChange={(newAttrs: any) => {
                const rects = rectangles.slice();
                rects[i] = newAttrs;
                setRectangles(rects);
              }}
            />
          );
        })}
        {adding && <Rect fill={color_map[label] + '4D'} x={adding[0]} y={adding[1]} width={adding[2] - adding[0]} height={adding[3] - adding[1]} />}
      </Layer>
    </Stage>
  );
};