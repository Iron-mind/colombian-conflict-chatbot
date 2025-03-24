import os
import json

def procesar_archivos(directorio):
    datos_archivos = []
    max_palabras = 0
    archivo_max = ""

    for entrada in os.scandir(directorio):
        if entrada.is_file():
            try:
                with open(entrada.path, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read()
                    palabras = contenido.split()
                    num_palabras = len(palabras)
                    
                    # Agregar a la lista de resultados
                    datos_archivos.append({
                        "name": entrada.name,
                        "count": num_palabras
                    })
                    
                    # Actualizar máximo
                    if num_palabras > max_palabras:
                        max_palabras = num_palabras
                        archivo_max = entrada.name

            except Exception as e:
                print(f"Error procesando {entrada.name}: {str(e)}")

    # Guardar en JSON
    with open('resultados.json', 'w', encoding='utf-8') as json_file:
        json.dump(datos_archivos, json_file, indent=4)

    # Mostrar resultado máximo si hay archivos procesados
    if archivo_max:
        print(f"\nArchivo con más palabras: {archivo_max}")
        print(f"Total de palabras: {max_palabras}")
    else:
        print("\nNo se encontraron archivos procesables")

if __name__ == "__main__":
    directorio = input("Ingrese la ruta del directorio a analizar (deje vacío para usar el actual): ").strip()
    if not directorio:
        directorio = os.getcwd()
    
    if not os.path.isdir(directorio):
        print("El directorio especificado no existe")
    else:
        procesar_archivos(directorio)