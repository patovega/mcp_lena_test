 
import json
from main import lena_analyzer

def main():
    print("=== ANÁLISIS DE LENA ===")
    
    # Análisis completo
    print("\n1. Análisis completo:")
    result = lena_analyzer.analyze_lena_complete()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Solo detección de rostros
    print("\n2. Detección de rostros:")
    faces = lena_analyzer.detect_faces_only()
    print(json.dumps(faces, indent=2, ensure_ascii=False))
    
    # Crear visualizaciones
    print("\n3. Creando visualizaciones...")
    visual = lena_analyzer.create_visual_analysis()
    print(json.dumps(visual, indent=2, ensure_ascii=False))
    
    print("\n¡Análisis completado!")

if __name__ == "__main__":
    main()
