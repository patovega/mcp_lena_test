# MCP Lena Test 🎭

Un servidor MCP (Model Context Protocol) para análisis de computer vision usando la famosa imagen de Lena.

## ¿Qué es esto?

Este proyecto demuestra cómo usar **MCP** para integrar algoritmos de computer vision con Claude. El servidor descarga automáticamente la icónica imagen de Lena y permite a Claude analizarla usando OpenCV.

## Características

- ✅ **Descarga automática** de la imagen de Lena
- 👤 **Detección de rostros** usando HaarCascade
- 👁️ **Detección de ojos** dentro de rostros
- 🎨 **Análisis de colores** (RGB promedio)
- 🔲 **Detección de bordes** con algoritmo Canny
- ☀️ **Análisis de brillo y contraste**
- 📸 **Generación de visualizaciones** con detecciones marcadas

## Instalación

```bash
git clone https://github.com/patovega/mcp_lena_test.git
cd mcp_lena_test
pip install -r requirements.txt
```

### Requirements

```
mcp
opencv-python
numpy
requests
```

## Configuración

### Claude Desktop

1. Instalar [Claude Desktop](https://claude.ai/download)
2. Configurar MCP en `claude_desktop_config.json`:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "lena-analysis": {
      "command": "python",
      "args": ["/ruta/completa/a/main.py"]
    }
  }
}
```

3. Reiniciar Claude Desktop

## Uso

### Ejecutar el servidor

```bash
python main.py
```

### Demo en Claude Desktop

Acceso a herramiantas en claude

![image](https://github.com/user-attachments/assets/0222d332-a14f-4c4b-89aa-ae1bee323bc2)


Solicitud de permisos
![image](https://github.com/user-attachments/assets/ab74e07a-f4bb-4567-92d4-403f6fd6c0da)

*Claude Desktop mostrando las herramientas MCP disponibles para análisis de Lena*

### Comandos disponibles en Claude

Una vez configurado, puedes usar estos comandos en Claude Desktop:

- **Análisis completo:** *"Claude, analiza la imagen de Lena"*
- **Solo rostros:** *"Claude, detecta rostros en Lena"*
- **Crear visualizaciones:** *"Claude, crea las visualizaciones de Lena"*
- **Descargar imagen fresca:** *"Claude, descarga una copia nueva de Lena"*

## Herramientas MCP disponibles

- `analyze_lena` - Análisis completo de la imagen
- `detect_faces_lena` - Detección específica de rostros
- `create_visual_lena` - Generar imágenes con detecciones marcadas  
- `download_fresh_lena` - Descargar nueva copia de la imagen

## Ejemplo de salida

```json
{
  "image_info": {
    "dimensions": "512x512",
    "channels": 3,
    "file_size": 473831
  },
  "face_detection": {
    "faces_count": 1,
    "faces_details": [
      {
        "id": 1,
        "position": {"x": 214, "y": 202},
        "size": {"width": 150, "height": 150},
        "eyes_detected": 2
      }
    ]
  },
  "color_analysis": {
    "average_rgb": [180, 130, 120]
  },
  "edge_analysis": {
    "edge_density_percentage": 8.2,
    "complexity": "Media"
  },
  "brightness_contrast": {
    "brightness": 145.6,
    "contrast": 42.3
  }
}
```

## Estructura del proyecto

```
mcp_lena_test/
├── main.py              # Servidor MCP principal
├── run.py               # Script de prueba/demo
├── lena_demo/          # Resultados generados
│   ├── lena.png
│   ├── lena_with_detection.jpg
│   └── lena_edges.jpg

```
 
## Resultados

El programa crea una carpeta `lena_demo/` con:

- `lena.png` - Imagen original descargada
- `lena_with_detection.jpg` - Imagen con rostros y ojos marcados
- `lena_edges.jpg` - Detección de bordes

 
