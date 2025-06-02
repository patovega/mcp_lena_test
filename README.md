# MCP Lena Test 🎭🗄️

Un proyecto completo de **Model Context Protocol (MCP)** que demuestra dos casos de uso avanzados:
- 🖼️ **Computer Vision** con la famosa imagen de Lena
- 🗄️ **Business Intelligence** con análisis de base de datos

## 🎯 ¿Qué es esto?

Este proyecto muestra el poder de **MCP** para integrar diferentes tipos de análisis con Claude:
1. **Análisis de Computer Vision** usando OpenCV
2. **Analytics de Negocio** con base de datos SQLite y consultas inteligentes

## 🚀 Características

### 🖼️ **Servidor de Computer Vision** (`main.py`)
- ✅ **Descarga automática** de la imagen de Lena
- 👤 **Detección de rostros** usando HaarCascade
- 👁️ **Detección de ojos** dentro de rostros
- 🎨 **Análisis de colores** (RGB promedio)
- 🔲 **Detección de bordes** con algoritmo Canny
- ☀️ **Análisis de brillo y contraste**
- 📸 **Generación de visualizaciones** con detecciones marcadas

### 🗄️ **Servidor de Business Intelligence** (`database_server.py`)
- 📊 **KPIs automáticos** (ingresos, clientes, pedidos)
- 🤖 **Preguntas en lenguaje natural** ("mejores clientes", "productos más vendidos")
- 📈 **Reportes automáticos** (ventas, clientes, productos)
- 🔍 **Descubrimiento de insights** automático
- ⚠️ **Alertas de inventario** y productos sin ventas
- 💡 **Analytics avanzados** con JOIN queries complejas

## 📁 Estructura del Proyecto

```
MCP_LENA_TEST/
├── 🖼️ COMPUTER VISION
│   ├── main.py                     # Servidor MCP para análisis de imágenes
│   ├── run.py                      # Demo del análisis de Lena
│   └── lena_demo/                  # Resultados generados
│       ├── lena.png               # Imagen original
│       ├── lena_with_detection.jpg # Con detección de rostros
│       └── lena_edges.jpg         # Detección de bordes
│
├── 🗄️ BUSINESS INTELLIGENCE  
│   ├── database_server.py          # Servidor MCP para análisis de datos
│   ├── database_demo.py           # Demo completo de capacidades
│   ├── mcp_database.db           # Base de datos SQLite
│   └── database_demo/            # Carpeta adicional de demos
│
├── ⚙️ CONFIGURACIÓN
│   ├── claude_desktop_config.json        # Configuración real de Claude
│   ├── claude_desktop_config_template.json # Template de configuración
│   ├── requirements.txt                   # Dependencias
│   └── README.md                         # Esta documentación
│
└── 🗂️ GENERATED
    └── __pycache__/                      # Cache de Python
```

## 🛠️ Instalación

```bash
git clone https://github.com/patovega/mcp_lena_test.git
cd MCP_LENA_TEST
pip install -r requirements.txt
```

### 📦 Requirements

```
mcp
opencv-python
numpy
requests
sqlite3
asyncio
```

## ⚙️ Configuración

### Claude Desktop

1. Instalar [Claude Desktop](https://claude.ai/download)
2. Configurar **ambos servidores** en tu archivo de configuración:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "lena-vision": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/ruta/completa/a/MCP_LENA_TEST"
    },
    "business-intelligence": {
      "command": "python", 
      "args": ["database_server.py"],
      "cwd": "/ruta/completa/a/MCP_LENA_TEST"
    }
  }
}
```

3. Reiniciar Claude Desktop

## 🎮 Uso

### 🖼️ **Computer Vision**

```bash
# Ejecutar servidor de visión
python main.py

# Demo standalone
python run.py
```

**Comandos en Claude:**
- *"Claude, analiza la imagen de Lena"*
- *"Claude, detecta rostros en Lena"*
- *"Claude, crea visualizaciones de Lena"*

### 🗄️ **Business Intelligence**

```bash
# Ejecutar servidor de BD
python database_server.py

# Demo completo de capacidades
python database_demo.py
```

**Comandos en Claude:**
- *"¿Cuáles son mis KPIs principales?"*
- *"¿Quiénes son mis mejores clientes?"*
- *"Dame un reporte de ventas"*
- *"¿Qué productos necesito reabastecer?"*
- *"Encuentra insights en mis datos"*

## 🔧 Herramientas MCP Disponibles

### 🖼️ **Computer Vision Tools**
- `analyze_lena` - Análisis completo de la imagen
- `detect_faces_lena` - Detección específica de rostros
- `create_visual_lena` - Generar imágenes con detecciones marcadas  
- `download_fresh_lena` - Descargar nueva copia de la imagen

### 🗄️ **Business Intelligence Tools**
- `execute_query` - Ejecutar consultas SQL SELECT
- `ask_business_question` - Preguntas en lenguaje natural
- `get_kpis` - Indicadores clave de rendimiento
- `generate_business_report` - Reportes automáticos
- `find_insights` - Descubrimiento de insights
- `get_sales_analytics` - Análisis de ventas avanzado
- `get_customer_insights` - Insights de clientes
- `get_inventory_alerts` - Alertas de inventario
- `get_table_schema` - Estructura de tablas
- `get_database_stats` - Estadísticas de la BD

## 📊 Ejemplo de Datos

### 🖼️ **Análisis de Lena**
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
  }
}
```

### 🗄️ **KPIs de Negocio**
```json
{
  "active_customers": 7,
  "completed_orders": 6,
  "total_revenue": 12749.91,
  "avg_order_value": 2124.99,
  "total_products": 13,
  "low_stock_products": 3,
  "orders_per_customer": 0.86
}
```

## 🎯 Casos de Uso

### 🎭 **Para Desarrolladores de CV**
- Análisis automatizado de imágenes
- Integración de OpenCV con Claude
- Detección de objetos y características

### 📈 **Para Analistas de Datos**
- Business Intelligence conversacional
- KPIs automáticos en tiempo real
- Reportes generados por IA
- Descubrimiento de insights

### 🔬 **Para Investigadores de MCP**
- Ejemplos completos de servidores MCP
- Integración multi-modal (visión + datos)
- Patrones de diseño para herramientas MCP

## 🔄 Demo Completo

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Probar Computer Vision
python run.py

# 3. Probar Business Intelligence  
python database_demo.py

# 4. Configurar Claude Desktop
# (copiar config template)

# 5. ¡Usar ambos en Claude!
```

## 🏆 Resultados

### 🖼️ **Computer Vision**
Genera `lena_demo/` con:
- `lena.png` - Imagen original
- `lena_with_detection.jpg` - Con rostros detectados
- `lena_edges.jpg` - Detección de bordes

### 🗄️ **Business Intelligence**
Crea `mcp_database.db` con:
- 8 usuarios de diferentes países
- 13 productos en múltiples categorías
- 8 pedidos con estados variados
- Relaciones completas entre entidades
