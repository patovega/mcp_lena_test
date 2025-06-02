import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_advanced_demo():
    
    # Configuración del servidor inteligente
    server_params = StdioServerParameters(
        command="python",
        args=["database_demo/database_server.py"],  # Usa el servidor avanzado
    )
    
    print(" Iniciando Demo")
    print("=" * 70)
    print("Este demo muestra a Claude interactuando como analista de datos")
    print("usando MCP como interfaz a una BD.")
    print()
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()
            
            # 1. Mostrar capacidades inteligentes
            print("1. Herramientas Disponibles:")
            print("-" * 50)
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"{tool.name}")
                print(f"{tool.description}")
                print()
            
            print("2. Dashboard de KPIs en Tiempo Real:")
            print("-" * 50)
            result = await session.call_tool("get_kpis", {})
            print(result.content[0].text)
            print()
            
            business_questions = [
                "mejores clientes",
                "productos más vendidos", 
                "ventas por país",
                "clientes inactivos",
                "inventario bajo"
            ]
            
            print("3. Análisis con Preguntas de Negocio:")
            print("-" * 50)
            
            for i, question in enumerate(business_questions, 1):
                print(f"Pregunta {i}: ¿Cuáles son los {question}?")
                result = await session.call_tool("ask_business_question", {
                    "question": question
                })
                
                response = result.content[0].text
                if "Respuesta a:" in response:
                    lines = response.split('\n')
                    print(f"{lines[0]}")

                    try:
                        data_start = response.find('[')
                        if data_start != -1:
                            data_json = response[data_start:]
                            data = json.loads(data_json)
                            if data and len(data) > 0:
                                print(f"encontrados {len(data)} resultados")
                                if isinstance(data[0], dict):
                                    first_item = data[0]
                                    key_info = ', '.join([f"{k}: {v}" for k, v in list(first_item.items())[:3]])
                                    print(f"ejemplo: {key_info}")
                    except:
                        print("3.1 Datos procesados exitosamente")
                else:
                    print(f"3.1 response: {response}")
                print()
            
            print("4. Generación Automática de Reportes:")
            print("-" * 50)
            
            report_types = ["sales", "customers", "products"]
            for report_type in report_types:
                print(f"Generando reporte de {report_type}...")
                result = await session.call_tool("generate_business_report", {
                    "report_type": report_type,
                    "period": "month"
                })
                
                response = result.content[0].text
                lines = response.split('\n')
                print(f"{lines[0] if lines else 'Reporte generado'}")
                
                if "summary" in response.lower():
                    try:
                        data_start = response.find('{')
                        if data_start != -1:
                            data_json = response[data_start:]
                            data = json.loads(data_json)
                            if 'summary' in data:
                                summary = data['summary']
                                print(f"Resumen: {summary}")
                    except:
                        pass
                print()
            
            print("5. Descubrimiento Automático de Insights:")
            print("-" * 50)
            
            focus_areas = ["sales", "customers", "products"]
            for area in focus_areas:
                print(f"Analizando área: {area}")
                result = await session.call_tool("find_insights", {
                    "focus_area": area
                })
                
                response = result.content[0].text
                print(response)
                print()
            

            print("6. Análisis Integral del Negocio:")
            print("-" * 50)
            result = await session.call_tool("find_insights", {
                "focus_area": "all"
            })
            print(result.content[0].text)
            print()
            
            print("7. Simulación de Conversación con Claude:")
            print("-" * 50)
            
            conversation_scenarios = [
                ("¿Cómo está mi negocio?", "get_kpis"),
                ("¿Quiénes compran más?", "ask_business_question", {"question": "mejores clientes"}),
                ("¿Qué productos necesito reabastecer?", "ask_business_question", {"question": "inventario bajo"}),
                ("Dame un reporte de ventas", "generate_business_report", {"report_type": "sales", "period": "month"})
            ]
            
            for i, scenario in enumerate(conversation_scenarios, 1):
                user_question = scenario[0]
                tool_name = scenario[1]
                tool_args = scenario[2] if len(scenario) > 2 else {}
                
                print(f"Usuario: {user_question}")
                print(f"Claude: Analicemos esto... [llamando a {tool_name}]")
                
                result = await session.call_tool(tool_name, tool_args)
                response = result.content[0].text
                
          
                if len(response) > 200:
                    summary = response[:200] + "..."
                    print(f"claude: Aquí tienes el análisis: {summary}")
                else:
                    print(f"claude: {response}")
                print()
    
    print("Demo final")
    print("=" * 70)
    print()
    print("Base de datos: enhanced_mcp_database.db")
    print("Servidor: database_server.py")


if __name__ == "__main__":
    asyncio.run(run_advanced_demo())