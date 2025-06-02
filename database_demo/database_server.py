import asyncio
import sqlite3
import json
from typing import Any
from datetime import datetime, timedelta
import random
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

class CompleteDatabaseMCP:
    def __init__(self, db_path: str = "database_demo/mcp_database.db"):
        self.db_path = db_path
        self.server = Server("complete-database-mcp")
        self._setup_handlers()
        self._init_database()
    
    def _init_database(self):
        """Inicializa la base de datos con todas las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER,
                country TEXT,
                registration_date DATE,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
          
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                price REAL NOT NULL,
                cost REAL,
                stock INTEGER DEFAULT 0,
                supplier TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                order_date DATE,
                total_amount REAL,
                status TEXT DEFAULT 'pending',
                shipping_country TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            self._insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def _insert_sample_data(self, cursor):
        """Inserta datos de ejemplo"""
        
        # Usuarios
        sample_users = [
            ("Juan Pérez", "juan@email.com", 30, "España", "2024-01-15", 1),
            ("Ana García", "ana@email.com", 25, "México", "2024-02-20", 1),
            ("Carlos López", "carlos@email.com", 35, "Argentina", "2024-01-10", 1),
            ("María Rodríguez", "maria@email.com", 28, "Chile", "2024-03-05", 1),
            ("Pedro Martín", "pedro@email.com", 42, "Colombia", "2024-02-28", 1),
            ("Sofia Chen", "sofia@email.com", 31, "Perú", "2024-01-20", 0),  # Cliente inactivo
            ("Roberto Silva", "roberto@email.com", 29, "Brasil", "2024-03-15", 1),
            ("Isabella Santos", "isabella@email.com", 26, "Uruguay", "2024-02-10", 1)
        ]
        cursor.executemany(
            "INSERT INTO users (name, email, age, country, registration_date, is_active) VALUES (?, ?, ?, ?, ?, ?)",
            sample_users
        )
        
        # Productos
        sample_products = [
            ("MacBook Pro", "Electronics", 2499.99, 1800.00, 5, "Apple"),  # Stock bajo
            ("iPhone 15", "Electronics", 1199.99, 850.00, 32, "Apple"),
            ("AirPods Pro", "Electronics", 249.99, 150.00, 8, "Apple"),  # Stock bajo
            ("Samsung Galaxy S24", "Electronics", 999.99, 700.00, 28, "Samsung"),
            ("Dell XPS 13", "Electronics", 1299.99, 950.00, 20, "Dell"),
            ("Sony WH-1000XM5", "Electronics", 399.99, 250.00, 3, "Sony"),  # Stock muy bajo
            
            ("Escritorio Ejecutivo", "Furniture", 599.99, 350.00, 12, "IKEA"),
            ("Silla Ergonómica", "Furniture", 299.99, 180.00, 15, "Herman Miller"),
            ("Estantería", "Furniture", 189.99, 120.00, 6, "IKEA"),  # Stock bajo
            
            ("Cafetera Espresso", "Kitchen", 299.99, 180.00, 22, "Breville"),
            ("Licuadora", "Kitchen", 89.99, 55.00, 35, "Vitamix"),
            ("Tostadora", "Kitchen", 129.99, 80.00, 25, "Cuisinart"),
            
            ("Producto sin ventas", "Electronics", 199.99, 100.00, 50, "NoSales Inc")  # Sin ventas
        ]
        cursor.executemany(
            "INSERT INTO products (name, category, price, cost, stock, supplier) VALUES (?, ?, ?, ?, ?, ?)",
            sample_products
        )

        orders_data = [
            (1, "2024-03-01", "completed", "España"),
            (2, "2024-03-05", "completed", "México"), 
            (3, "2024-03-10", "shipped", "Argentina"),
            (4, "2024-03-15", "completed", "Chile"),
            (5, "2024-03-20", "pending", "Colombia"),
            (1, "2024-03-25", "completed", "España"),
            (4, "2024-03-28", "shipped", "Chile"),
            (2, "2024-04-01", "completed", "México")
        ]
        
        for i, (user_id, order_date, status, shipping_country) in enumerate(orders_data, 1):
            cursor.execute(
                "INSERT INTO orders (user_id, order_date, total_amount, status, shipping_country) VALUES (?, ?, ?, ?, ?)",
                (user_id, order_date, 0, status, shipping_country) 
            )
        
        # Detalles de pedidos
        order_items_data = [
            (1, 1, 1, 2499.99),  # MacBook
            (1, 3, 2, 249.99),   # AirPods x2
            (2, 2, 1, 1199.99),  # iPhone
            (3, 5, 1, 1299.99),  # Dell XPS
            (3, 6, 1, 399.99),   # Sony headphones
            (4, 4, 2, 999.99),   # Samsung x2
            (5, 7, 1, 599.99),   # Escritorio
            (6, 1, 1, 2499.99),  # MacBook
            (7, 8, 1, 299.99),   # Silla
            (8, 11, 3, 89.99),   # Licuadora x3
        ]
        
        for order_id, product_id, quantity, unit_price in order_items_data:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, unit_price)
            )
        
        cursor.execute("""
            UPDATE orders SET total_amount = (
                SELECT SUM(quantity * unit_price)
                FROM order_items
                WHERE order_items.order_id = orders.id
            )
        """)
    
    def _setup_handlers(self):
        """Configura TODOS los handlers necesarios"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """Lista TODAS las herramientas disponibles"""
            return [
                types.Tool(
                    name="execute_query",
                    description="Ejecuta una consulta SQL SELECT",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Consulta SQL SELECT a ejecutar"}
                        },
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="get_table_schema",
                    description="Obtiene el schema de una tabla",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table_name": {"type": "string", "description": "Nombre de la tabla"}
                        },
                        "required": ["table_name"]
                    }
                ),
                types.Tool(
                    name="get_database_stats",
                    description="Obtiene estadísticas de la base de datos",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="ask_business_question",
                    description="Responde preguntas de negocio en lenguaje natural",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "question": {"type": "string", "description": "Pregunta de negocio en lenguaje natural"}
                        },
                        "required": ["question"]
                    }
                ),
                types.Tool(
                    name="get_kpis",
                    description="Obtiene indicadores clave de rendimiento (KPIs)",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="generate_business_report",
                    description="Genera reportes de negocio automáticamente",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "report_type": {
                                "type": "string",
                                "enum": ["sales", "customers", "products"],
                                "description": "Tipo de reporte a generar"
                            },
                            "period": {
                                "type": "string",
                                "enum": ["week", "month", "quarter"],
                                "description": "Período del reporte"
                            }
                        },
                        "required": ["report_type"]
                    }
                ),
                types.Tool(
                    name="find_insights",
                    description="Encuentra insights automáticamente en los datos",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "focus_area": {
                                "type": "string",
                                "enum": ["sales", "customers", "products", "all"],
                                "description": "Área de enfoque para los insights"
                            }
                        }
                    }
                ),
                types.Tool(
                    name="get_sales_analytics",
                    description="Obtiene análisis de ventas avanzado",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "period": {"type": "string", "enum": ["week", "month", "quarter"], "description": "Período de análisis"}
                        }
                    }
                ),
                types.Tool(
                    name="get_customer_insights",
                    description="Obtiene insights de clientes",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="get_inventory_alerts",
                    description="Obtiene alertas de inventario",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> list[types.TextContent]:
            """Maneja TODAS las llamadas a herramientas"""
            if arguments is None:
                arguments = {}
            
            try:
                if name == "execute_query":
                    return await self._execute_query(arguments.get("query", ""))
                elif name == "get_table_schema":
                    return await self._get_table_schema(arguments.get("table_name", ""))
                elif name == "get_database_stats":
                    return await self._get_database_stats()
                elif name == "ask_business_question":
                    return await self._ask_business_question(arguments.get("question", ""))
                elif name == "get_kpis":
                    return await self._get_kpis()
                elif name == "generate_business_report":
                    return await self._generate_business_report(
                        arguments.get("report_type", "sales"),
                        arguments.get("period", "month")
                    )
                elif name == "find_insights":
                    return await self._find_insights(arguments.get("focus_area", "all"))
                elif name == "get_sales_analytics":
                    return await self._get_sales_analytics(arguments.get("period", "month"))
                elif name == "get_customer_insights":
                    return await self._get_customer_insights()
                elif name == "get_inventory_alerts":
                    return await self._get_inventory_alerts()
                
                else:
                    raise ValueError(f"Herramienta desconocida: {name}")
            
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
    
    async def _execute_query(self, query: str) -> list[types.TextContent]:
        """Ejecuta una consulta SQL SELECT"""
        if not query.strip().upper().startswith("SELECT"):
            return [types.TextContent(
                type="text",
                text="Error: Solo se permiten consultas SELECT"
            )]
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            data = [dict(row) for row in results]
            
            return [types.TextContent(
                type="text",
                text=f"Consulta ejecutada exitosamente.\nResultados:\n{json.dumps(data, indent=2, default=str)}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error ejecutando consulta: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def _get_table_schema(self, table_name: str) -> list[types.TextContent]:
        """Obtiene el schema de una tabla"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"PRAGMA table_info({table_name})")
            schema = cursor.fetchall()
            
            if not schema:
                return [types.TextContent(
                    type="text",
                    text=f"La tabla '{table_name}' no existe"
                )]
            
            schema_info = []
            for column in schema:
                schema_info.append({
                    "column_id": column[0],
                    "name": column[1],
                    "type": column[2],
                    "not_null": bool(column[3]),
                    "default_value": column[4],
                    "primary_key": bool(column[5])
                })
            
            return [types.TextContent(
                type="text",
                text=f"Schema de la tabla '{table_name}':\n{json.dumps(schema_info, indent=2)}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error obteniendo schema: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def _get_database_stats(self) -> list[types.TextContent]:
        """Obtiene estadísticas de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            stats = {"tables": {}}
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                stats["tables"][table_name] = {"row_count": count}
            
            return [types.TextContent(
                type="text",
                text=f"Estadisticas de la base de datos:\n{json.dumps(stats, indent=2)}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error obteniendo estadísticas: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def _ask_business_question(self, question: str) -> list[types.TextContent]:
        """Responde preguntas de negocio en lenguaje natural"""
        question_lower = question.lower()
        
        # ampliamos el mapeo de preguntas
        query_patterns = {
            "mejores clientes": """
                SELECT u.name, u.email, u.country, 
                       COUNT(o.id) as total_orders,
                       SUM(o.total_amount) as total_spent
                FROM users u
                JOIN orders o ON u.id = o.user_id
                WHERE o.status = 'completed'
                GROUP BY u.id
                ORDER BY total_spent DESC
                LIMIT 5
            """,
            
            "productos más vendidos": """
                SELECT p.name, p.category, 
                       SUM(oi.quantity) as total_sold,
                       SUM(oi.quantity * oi.unit_price) as revenue,
                       p.supplier
                FROM products p
                JOIN order_items oi ON p.id = oi.product_id
                JOIN orders o ON oi.order_id = o.id
                WHERE o.status IN ('completed', 'shipped')
                GROUP BY p.id
                ORDER BY total_sold DESC
                LIMIT 5
            """,
            
            "ventas por país": """
                SELECT u.country, 
                       COUNT(o.id) as total_orders,
                       SUM(o.total_amount) as total_revenue,
                       AVG(o.total_amount) as avg_order_value
                FROM users u
                JOIN orders o ON u.id = o.user_id
                WHERE o.status = 'completed'
                GROUP BY u.country
                ORDER BY total_revenue DESC
            """,
            
            "clientes inactivos": """
                SELECT name, email, country, registration_date
                FROM users
                WHERE is_active = 0 OR id NOT IN (
                    SELECT DISTINCT user_id FROM orders WHERE status = 'completed'
                )
            """,
            
            "inventario bajo": """
                SELECT name, category, stock, price, supplier
                FROM products
                WHERE stock < 10
                ORDER BY stock ASC
            """
        }
        
        selected_query = None
        for pattern, query in query_patterns.items():
            if pattern in question_lower:
                selected_query = query
                break
        
        if not selected_query:
            available_questions = ", ".join(query_patterns.keys())
            return [types.TextContent(
                type="text",
                text=f"Pregunta no reconocida. Prueba: {available_questions}"
            )]

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(selected_query)
            results = cursor.fetchall()
            data = [dict(row) for row in results]
            
            return [types.TextContent(
                type="text",
                text=f"Respuesta a: '{question}'\n\n{json.dumps(data, indent=2, default=str)}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def _get_kpis(self) -> list[types.TextContent]:
        """Obtiene indicadores clave de rendimiento"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # KPIs principales
            cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM users WHERE is_active = 1) as active_customers,
                    (SELECT COUNT(*) FROM orders WHERE status = 'completed') as completed_orders,
                    (SELECT SUM(total_amount) FROM orders WHERE status = 'completed') as total_revenue,
                    (SELECT AVG(total_amount) FROM orders WHERE status = 'completed') as avg_order_value,
                    (SELECT COUNT(*) FROM products) as total_products,
                    (SELECT COUNT(*) FROM products WHERE stock < 10) as low_stock_products
            """)
            
            kpis = dict(cursor.fetchone())
            
            # Calcular métricas adicionales
            if kpis['completed_orders'] and kpis['active_customers']:
                kpis['orders_per_customer'] = round(kpis['completed_orders'] / kpis['active_customers'], 2)
            
            return [types.TextContent(
                type="text",
                text=f"KPIs del Negocio:\n\n{json.dumps(kpis, indent=2, default=str)}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error calculando KPIs: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def _generate_business_report(self, report_type: str, period: str) -> list[types.TextContent]:
        """Genera reportes de negocio automáticamente"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            if report_type == "sales":
                cursor.execute("""
                    SELECT 
                        DATE(o.order_date) as date,
                        COUNT(*) as orders_count,
                        SUM(o.total_amount) as daily_revenue,
                        AVG(o.total_amount) as avg_order_value
                    FROM orders o
                    WHERE o.status IN ('completed', 'shipped')
                    GROUP BY DATE(o.order_date)
                    ORDER BY date DESC
                """)
                sales_data = [dict(row) for row in cursor.fetchall()]
                
                cursor.execute("""
                    SELECT 
                        SUM(total_amount) as total_revenue,
                        COUNT(*) as total_orders,
                        AVG(total_amount) as avg_order_value
                    FROM orders
                    WHERE status IN ('completed', 'shipped')
                """)
                summary = dict(cursor.fetchone())
                
                report_data = {
                    "report_type": "Sales Report",
                    "period": period,
                    "summary": summary,
                    "daily_sales": sales_data
                }
                
            elif report_type == "customers":
                cursor.execute("""
                    SELECT country, COUNT(*) as customer_count,
                           SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active_count
                    FROM users
                    GROUP BY country
                    ORDER BY customer_count DESC
                """)
                by_country = [dict(row) for row in cursor.fetchall()]
                
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_customers,
                        SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active_customers
                    FROM users
                """)
                summary = dict(cursor.fetchone())
                
                report_data = {
                    "report_type": "Customer Report",
                    "period": period,
                    "summary": summary,
                    "by_country": by_country
                }
                
            elif report_type == "products":
                cursor.execute("""
                    SELECT category, COUNT(*) as product_count,
                           AVG(price) as avg_price,
                           SUM(stock) as total_stock
                    FROM products
                    GROUP BY category
                    ORDER BY product_count DESC
                """)
                by_category = [dict(row) for row in cursor.fetchall()]
                
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_products,
                        COUNT(CASE WHEN stock < 10 THEN 1 END) as low_stock_count,
                        AVG(price) as avg_price
                    FROM products
                """)
                summary = dict(cursor.fetchone())
                
                report_data = {
                    "report_type": "Product Report", 
                    "period": period,
                    "summary": summary,
                    "by_category": by_category
                }
            
            return [types.TextContent(
                type="text",
                text=f"{report_data['report_type']} - {period}\n\n{json.dumps(report_data, indent=2, default=str)}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error generando reporte: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def _find_insights(self, focus_area: str) -> list[types.TextContent]:
        """Encuentra insights automáticamente"""
        insights = []
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            if focus_area in ["sales", "all"]:
                # Insight de producto más rentable
                cursor.execute("""
                    SELECT p.name, 
                           (p.price - p.cost) as profit_per_unit,
                           COALESCE(SUM(oi.quantity), 0) as units_sold,
                           COALESCE(SUM((p.price - p.cost) * oi.quantity), 0) as total_profit
                    FROM products p
                    LEFT JOIN order_items oi ON p.id = oi.product_id
                    LEFT JOIN orders o ON oi.order_id = o.id AND o.status = 'completed'
                    WHERE p.cost IS NOT NULL AND p.cost > 0
                    GROUP BY p.id
                    ORDER BY total_profit DESC
                    LIMIT 1
                """)
                most_profitable = cursor.fetchone()
                if most_profitable and most_profitable['total_profit'] > 0:
                    insights.append(f"producto más rentable: {most_profitable['name']} con ${most_profitable['total_profit']:.2f} en ganancias totales")
            
            if focus_area in ["customers", "all"]:
                #país con más clientes
                cursor.execute("""
                    SELECT country, COUNT(*) as customer_count
                    FROM users
                    WHERE is_active = 1
                    GROUP BY country
                    ORDER BY customer_count DESC
                    LIMIT 1
                """)
                top_country = cursor.fetchone()
                if top_country:
                    insights.append(f"pais con más clientes activos: {top_country['country']} ({top_country['customer_count']} clientes)")
            
            if focus_area in ["products", "all"]:
                #productos con bajo stock
                cursor.execute("""
                    SELECT COUNT(*) as low_stock_count
                    FROM products
                    WHERE stock < 10
                """)
                low_stock = cursor.fetchone()
                if low_stock and low_stock['low_stock_count'] > 0:
                    insights.append(f"⚠️ Alerta: {low_stock['low_stock_count']} productos tienen inventario bajo (< 10 unidades)")
                
                #productos sin ventas
                cursor.execute("""
                    SELECT COUNT(*) as no_sales_count
                    FROM products p
                    LEFT JOIN order_items oi ON p.id = oi.product_id
                    WHERE oi.product_id IS NULL
                """)
                no_sales = cursor.fetchone()
                if no_sales and no_sales['no_sales_count'] > 0:
                    insights.append(f"📊 {no_sales['no_sales_count']} productos no han tenido ventas aún")
            
            if not insights:
                insights.append("✅ Todo parece estar funcionando bien en esta área")
            
            insights_text = "\n".join([f"• {insight}" for insight in insights])
            
            return [types.TextContent(
                type="text",
                text=f"insights automáticos ({focus_area}):\n\n{insights_text}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error encontrando insights: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def _get_sales_analytics(self, period: str) -> list[types.TextContent]:
        """Obtiene análisis de ventas por período"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            #analisis general
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_orders,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value,
                    COUNT(DISTINCT user_id) as unique_customers
                FROM orders
                WHERE status = 'completed'
            """)
            summary = dict(cursor.fetchone())
            
            #ventas por categoria
            cursor.execute("""
                SELECT p.category,
                       COUNT(oi.id) as items_sold,
                       SUM(oi.quantity * oi.unit_price) as category_revenue
                FROM products p
                JOIN order_items oi ON p.id = oi.product_id
                JOIN orders o ON oi.order_id = o.id
                WHERE o.status = 'completed'
                GROUP BY p.category
                ORDER BY category_revenue DESC
            """)
            by_category = [dict(row) for row in cursor.fetchall()]
            
            analytics = {
                "period": period,
                "summary": summary,
                "by_category": by_category
            }
            
            return [types.TextContent(
                type="text",
                text=f"analisis de ventas ({period}):\n\n{json.dumps(analytics, indent=2, default=str)}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error en analisis: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def _get_customer_insights(self) -> list[types.TextContent]:
        """Obtiene insights de clientes"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            #clientes más valiosos
            cursor.execute("""
                SELECT u.name, u.country, 
                       COUNT(o.id) as order_count,
                       COALESCE(SUM(o.total_amount), 0) as lifetime_value
                FROM users u
                LEFT JOIN orders o ON u.id = o.user_id AND o.status = 'completed'
                WHERE u.is_active = 1
                GROUP BY u.id
                ORDER BY lifetime_value DESC
                LIMIT 3
            """)
            top_customers = [dict(row) for row in cursor.fetchall()]
            
            #distribución por país
            cursor.execute("""
                SELECT country, COUNT(*) as customer_count
                FROM users
                WHERE is_active = 1
                GROUP BY country
                ORDER BY customer_count DESC
            """)
            by_country = [dict(row) for row in cursor.fetchall()]
            
            insights = {
                "top_customers": top_customers,
                "distribution_by_country": by_country
            }
            
            return [types.TextContent(
                type="text",
                text=f"customer Insights:\n\n{json.dumps(insights, indent=2, default=str)}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def _get_inventory_alerts(self) -> list[types.TextContent]:
        """Obtiene alertas de inventario"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            #productos con stock bajo
            cursor.execute("""
                SELECT name, category, stock, supplier,
                       CASE WHEN cost IS NOT NULL THEN (price - cost) ELSE NULL END as profit_margin
                FROM products
                WHERE stock < 10
                ORDER BY stock ASC
            """)
            low_stock = [dict(row) for row in cursor.fetchall()]
            
            #productos sin ventas
            cursor.execute("""
                SELECT p.name, p.category, p.stock
                FROM products p
                LEFT JOIN order_items oi ON p.id = oi.product_id
                WHERE oi.product_id IS NULL
            """)
            no_sales = [dict(row) for row in cursor.fetchall()]
            
            alerts = {
                "low_stock_products": low_stock,
                "products_without_sales": no_sales
            }
            
            return [types.TextContent(
                type="text",
                text=f"alertas de inventario:\n\n{json.dumps(alerts, indent=2, default=str)}"
            )]
        
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
        
        finally:
            conn.close()
    
    async def run(self):
        """Ejecuta el servidor MCP"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="complete-database-mcp",
                    server_version="0.3.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


if __name__ == "__main__":
    complete_db_mcp = CompleteDatabaseMCP()
    asyncio.run(complete_db_mcp.run())