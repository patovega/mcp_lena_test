#!/usr/bin/env python3

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Sequence
import requests
import cv2
import numpy as np

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

app = Server("lena-analysis-mcp")

class LenaAnalysisDemo:
    def __init__(self):
        self.demo_folder = Path("lena_demo")
        self.demo_folder.mkdir(exist_ok=True)
        self.lena_url = "https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png"
        self.lena_path = self.demo_folder / "lena.png"
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    def download_lena(self):
        if self.lena_path.exists():
            return True
            
        try:
            response = requests.get(self.lena_url, timeout=10)
            response.raise_for_status()
            
            with open(self.lena_path, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            print(f"Error descargando Lena: {e}")
            return False
    
    def analyze_lena_complete(self):
        if not self.lena_path.exists():
            if not self.download_lena():
                return {"error": "No se pudo descargar Lena"}
        
        img = cv2.imread(str(self.lena_path))
        if img is None:
            return {"error": "No se pudo cargar la imagen"}
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        face_details = []
        if len(faces) > 0:
            for i, (x, y, w, h) in enumerate(faces):
                face_roi = gray[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(face_roi)
                face_details.append({
                    "id": i+1,
                    "position": {"x": int(x), "y": int(y)},
                    "size": {"width": int(w), "height": int(h)},
                    "eyes_detected": len(eyes)
                })
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        avg_color = np.mean(img_rgb.reshape(-1, 3), axis=0)
        
        edges = cv2.Canny(gray, 100, 200)
        edge_pixels = np.sum(edges > 0)
        edge_density = edge_pixels / (edges.shape[0] * edges.shape[1])
        
        brightness = np.mean(gray)
        contrast = np.std(gray)
        
        return {
            "image_info": {
                "dimensions": f"{img.shape[1]}x{img.shape[0]}",
                "channels": img.shape[2],
                "file_size": os.path.getsize(self.lena_path)
            },
            "face_detection": {
                "faces_count": len(faces),
                "faces_details": face_details
            },
            "color_analysis": {
                "average_rgb": [int(avg_color[0]), int(avg_color[1]), int(avg_color[2])]
            },
            "edge_analysis": {
                "edge_density_percentage": round(edge_density * 100, 2),
                "complexity": "Alta" if edge_density > 0.1 else "Media" if edge_density > 0.05 else "Baja"
            },
            "brightness_contrast": {
                "brightness": round(float(brightness), 2),
                "contrast": round(float(contrast), 2)
            }
        }
    
    def create_visual_analysis(self):
        if not self.lena_path.exists():
            if not self.download_lena():
                return {"error": "No se pudo descargar Lena"}
        
        img = cv2.imread(str(self.lena_path))
        if img is None:
            return {"error": "No se pudo cargar la imagen"}
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        img_with_faces = img.copy()
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img_with_faces, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face_roi = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(face_roi)
            
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(img_with_faces, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)
        
        edges = cv2.Canny(gray, 100, 200)
        
        output_faces = self.demo_folder / "lena_with_detection.jpg"
        output_edges = self.demo_folder / "lena_edges.jpg"
        
        cv2.imwrite(str(output_faces), img_with_faces)
        cv2.imwrite(str(output_edges), edges)
        
        return {
            "output_files": {
                "face_detection": str(output_faces),
                "edge_detection": str(output_edges)
            },
            "processing_complete": True
        }
    
    def detect_faces_only(self):
        if not self.lena_path.exists():
            if not self.download_lena():
                return {"error": "No se pudo descargar Lena"}
        
        img = cv2.imread(str(self.lena_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        return {
            "faces_detected": len(faces),
            "coordinates": [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} 
                          for (x, y, w, h) in faces]
        }

lena_analyzer = LenaAnalysisDemo()

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="analyze_lena",
            description="Análisis completo de la imagen de Lena: rostros, colores, bordes, brillo",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="detect_faces_lena",
            description="Detectar solo rostros en la imagen de Lena",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="create_visual_lena",
            description="Crear visualizaciones de Lena con detecciones marcadas",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="download_fresh_lena",
            description="Descargar una copia fresca de la imagen de Lena",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        if name == "analyze_lena":
            result = lena_analyzer.analyze_lena_complete()
            return [types.TextContent(
                type="text", 
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
            
        elif name == "detect_faces_lena":
            result = lena_analyzer.detect_faces_only()
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
            
        elif name == "create_visual_lena":
            result = lena_analyzer.create_visual_analysis()
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
            
        elif name == "download_fresh_lena":
            if lena_analyzer.lena_path.exists():
                os.remove(lena_analyzer.lena_path)
            
            success = lena_analyzer.download_lena()
            result = {
                "downloaded": success,
                "path": str(lena_analyzer.lena_path) if success else None
            }
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
            
        else:
            return [types.TextContent(
                type="text",
                text=f"Herramienta desconocida: {name}"
            )]
            
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error ejecutando {name}: {str(e)}"
        )]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="lena-analysis-mcp",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
