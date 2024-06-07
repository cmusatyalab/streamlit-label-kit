
// USING CIRCLE, MATRIX
import React, { useState, useEffect, useCallback} from 'react';
import { Stage, Layer, Rect, Image, Circle} from 'react-konva';
import {Mask} from '../../utils/Mask';


const KEY_NAMES = new Set<string>([
  "Delete", "Escape",
])

export interface SegmentCanvasProps {
  image: any,
  image_size: number[],
  scale: number;
  masks: Mask[];
  selectedId?: string | null,
  setSelectedId?: (selected: string | null) => void,
  setMasks?: (mask: Mask[]) => void,
  handleDelete?: any,
  color_map: any;
  mode: "display" | "edit" | "new",
  strokeSize?: number;
  strokeShape?: "circle" | "square",
  editMode?: "pen" | "erase",
  readOnly?: boolean,
}

export interface Segment{
  maskProps: Mask,
  onChange: any,
  isSelected: boolean,
  opacity: number,
  onClick: any,
  scale: number,
  edit?: boolean,
  strokeWidth?: number,
  readOnly?: boolean,
}

class HexToRgbConverter {
  private cache: { [key: string]: { r: number, g: number, b: number } } = {};

  hexToRgb(hex: string): { r: number, g: number, b: number } {
    if (this.cache[hex]) {
      return this.cache[hex];
    }

    const r = parseInt(hex.slice(1, 3), 16),
          g = parseInt(hex.slice(3, 5), 16),
          b = parseInt(hex.slice(5, 7), 16);

    this.cache[hex] = { r, g, b };
    return this.cache[hex];
  }
}

export const SegmentCanvas = ({ 
  image, 
  image_size, 
  scale, 
  masks,
  selectedId,
  setSelectedId,
  setMasks,
  handleDelete,
  color_map,
  mode="display",
  strokeSize=5,
  strokeShape="circle",
  editMode="pen",
  readOnly=false,
}: SegmentCanvasProps) => {
  const [drawing, setDrawing] = useState(false);
  const [canvasImage, setCanvasImage] = useState<HTMLCanvasElement>();
  const [cursor, setCursor] = useState<number[]>([0,0]);
  const [click, setClick] = useState<number[]>([0,0]);

  const converter = new HexToRgbConverter();

  const handleMouseDown = (e: any) => {
    if (mode === "edit" || mode === "new") {
      setDrawing(true);
      updateMask(e);
    } else {
      updateClick(e);
    }
    
  };

  const handleMouseMove = (e: any) => {
    if (drawing) {
      updateMask(e);
    }
    updateCursor(e);
  };

  const handleMouseUp = () => {
    setDrawing(false);
  };

  const handleKeyInteraction = useCallback((e: KeyboardEvent) => {
    if (e.type !== "keydown") {
      return
    }
    
    if (!KEY_NAMES.has(e.key) || selectedId === null) return;

    let updated = true

    if (updated && !readOnly && mode === "display") {
      let rects = [...masks];
      let index = rects.findIndex(rect => rect.id === selectedId);
      if (index === -1) return;

      switch (e.key) {
        case "Delete":
          handleDelete(selectedId);
          break;
        case "Escape":
          setSelectedId && setSelectedId(null);
          break;
      }
    }
    
    e.preventDefault();
  }, [masks, selectedId, setSelectedId, handleDelete, mode, readOnly]);

  const createImageFromMask = (masks: Mask[]) => {
    
    const width = image_size[0];
    const height = image_size[1];

    let canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    if (masks.length === 0) return canvas;

    if (ctx) {
      const imageData = ctx.createImageData(width, height);
      let data = imageData.data;
      
      const default_opacity = (mode === "display") ? 127 : 64;
      const selected_opacity = (mode === "display") ? 180 : 127;
   
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const index = (y * width + x) * 4;
          masks.map((mask) => {
            const color = color_map[mask.label] || '#FFFFFF';
            const { r, g, b } = converter.hexToRgb(color);
            
            const opacity = (selectedId === mask.id) ? selected_opacity : default_opacity;
            if (mask.data[y][x]) {
              data[index] = r;     // Red
              data[index + 1] = g; // Green
              data[index + 2] = b; // Blue
              data[index + 3] = opacity;
            } 
          });
        } 

      }
      // Streamlit.setComponentValue(default_opacity);
      ctx.putImageData(imageData, 0, 0);
      return canvas;
    }
    return null;
  };
  
  useEffect(() => {
    const canvas = createImageFromMask(masks);
    if (canvas) {
      setCanvasImage(canvas);
    }

    window.addEventListener('keydown', handleKeyInteraction);
    window.addEventListener('keyup', handleKeyInteraction);
    
    return () => {
      window.removeEventListener('keydown', handleKeyInteraction);
      window.removeEventListener('keyup', handleKeyInteraction);

    };
  }, [masks, image_size, mode, selectedId, click, handleKeyInteraction]);

  const updateClick = (e: any) => {
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    const x = Math.floor(point.x / scale);
    const y = Math.floor(point.y / scale);
    
    setClick([y, x]);

    if (masks.length === 0) return;

    let selected = false;
    masks.map((mask) => {
      if (mask.data[y][x]) {
        setSelectedId && setSelectedId(mask.id);
        selected = true;
      }
    });

    if (!selected) {
      setSelectedId && setSelectedId(null);
    }
  }

  const updateCursor = (e: any) => {
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    const x = Math.floor(point.x);
    const y = Math.floor(point.y);
    
    setCursor([y, x]);
  }

  const updateMask = (e: any) => {
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    const x = Math.floor(point.x / scale);
    const y = Math.floor(point.y / scale);
    const radius = Math.floor(strokeSize / 2); // Convert diameter to radius
    const radiusSquare = Math.floor(radius * radius);

    let new_masks = [...masks];
    let index = new_masks.findIndex(new_masks => new_masks.id === selectedId);
    if (index === -1) return;

    const height = new_masks[index].height
    const width = new_masks[index].width

    if (strokeSize === 1) {
      new_masks[index].data[y][x] = editMode === "pen";
    } else {
      for (let i = -radius; i <= radius; i++) {
        for (let j = -radius; j <= radius; j++) {
          const newY = y + i;
          const newX = x + j;

          if (strokeShape === "square") {
            if (newY >= 0 && newY < height && newX >= 0 && newX < width) {
              new_masks[index].data[newY][newX] = editMode === "pen";
            }
          } else if (strokeShape === "circle") {
            const distSq = i * i + j * j;
            if (distSq < radiusSquare + radius) { // Check if the point is within the circle
              if (newY >= 0 && newY < height && newX >= 0 && newX < width) {
                new_masks[index].data[newY][newX] = editMode === "pen";
              }
            }
          }
          
        }
      }
    }
    setMasks && setMasks(new_masks);
  };

  return (
    <Stage 
      width={image_size[0] * scale} 
      height={image_size[1] * scale}
      onMouseDown={handleMouseDown} 
      onMouseMove={handleMouseMove} 
      onMouseUp={handleMouseUp}
    >
      <Layer>
        <Image image={image} scaleX={scale} scaleY={scale} />
        {canvasImage && <Image image={canvasImage} scaleX={scale} scaleY={scale} />}
        {(mode !== "display") && (strokeShape === "square"? 
          <Rect 
              x={cursor[1] - (strokeSize / 2)} 
              y={cursor[0] - (strokeSize / 2)}
              width={strokeSize}
              height={strokeSize}
              fill='grey'
              opacity={0.5}
            /> : 
          <Circle
            x={cursor[1]} 
            y={cursor[0]}
            radius={Math.floor(strokeSize / 2) + 0.5}
            fill='grey'
            opacity={0.5}
          />)
          }
      </Layer>
    </Stage>
  );
};

export default SegmentCanvas;