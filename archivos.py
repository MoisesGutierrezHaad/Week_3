"""
archivos.py - Módulo para persistencia del inventario en formato CSV.
"""

import csv
import os

# Encabezado estándar del CSV
ENCABEZADO = ["nombre", "precio", "cantidad"]


def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        ruta (str): Ruta del archivo destino (ej: 'inventario.csv').
        incluir_header (bool): Si True, escribe la fila de encabezado.

    Retorna:
        bool: True si se guardó exitosamente, False si hubo error.
    """
    # Validar que el inventario no esté vacío
    if not inventario:
        print(" El inventario está vacío. No hay nada que guardar.")
        return False

    try:
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADO)

            if incluir_header:
                escritor.writeheader()  # Escribe: nombre,precio,cantidad

            escritor.writerows(inventario)  # Escribe cada producto

        print(f" Inventario guardado en: {ruta}")
        return True

    except PermissionError:
        print(f" Error: No tienes permisos para escribir en '{ruta}'.")
    except OSError as e:
        print(f" Error al guardar el archivo: {e}")

    return False


def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV con validaciones por fila.

    El archivo debe tener encabezado: nombre,precio,cantidad
    Las filas inválidas se omiten y se cuenta el total de errores.

    Parámetros:
        ruta (str): Ruta del archivo CSV a cargar.

    Retorna:
        tuple: (lista_productos, filas_invalidas)
               lista_productos (list): Productos válidos cargados.
               filas_invalidas (int): Cantidad de filas omitidas por error.
        None: Si el archivo no pudo abrirse.
    """
    productos = []
    filas_invalidas = 0

    try:
        with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            # Validar encabezado
            if lector.fieldnames != ENCABEZADO:
                print(f" El archivo no tiene el encabezado válido: {','.join(ENCABEZADO)}")
                print(f" Encabezado encontrado: {lector.fieldnames}")
                return None

            for numero_fila, fila in enumerate(lector, start=2):  # start=2 porque fila 1 es header
                try:
                    # Validar columnas exactas
                    if len(fila) != 3:
                        raise ValueError("Número de columnas incorrecto")

                    nombre = fila["nombre"].strip()
                    if not nombre:
                        raise ValueError("Nombre vacío")

                    precio = float(fila["precio"])
                    cantidad = int(fila["cantidad"])

                    # Valores no negativos
                    if precio < 0 or cantidad < 0:
                        raise ValueError("Precio o cantidad negativos")

                    productos.append({
                        "nombre": nombre,
                        "precio": precio,
                        "cantidad": cantidad
                    })

                except (ValueError, KeyError) as e:
                    filas_invalidas += 1  # Acumular errores sin detener la carga

        return productos, filas_invalidas

    except FileNotFoundError:
        print(f"  Archivo no encontrado: '{ruta}'")
    except UnicodeDecodeError:
        print(f"  El archivo '{ruta}' tiene un formato de texto no compatible.")
    except Exception as e:
        print(f" Error inesperado al leer el archivo: {e}")

    return None


def fusionar_inventarios(inventario_actual, productos_nuevos):
    """
    Fusiona productos nuevos en el inventario actual.

    Política de fusión:
      - Si el nombre ya existe: suma la cantidad y actualiza el precio al nuevo.
      - Si el nombre no existe: lo agrega al inventario.

    Parámetros:
        inventario_actual (list): Inventario en memoria.
        productos_nuevos (list): Productos cargados desde CSV.

    Retorna:
        int: Cantidad de productos fusionados (existentes actualizados).
    """
    print("\n  📋 Política de fusión: si el producto ya existe,")
    print("     se suma la cantidad y se actualiza el precio al nuevo valor.\n")

    fusionados = 0

    for nuevo in productos_nuevos:
        # Buscar si ya existe en el inventario actual
        existente = next(
            (p for p in inventario_actual if p["nombre"].lower() == nuevo["nombre"].lower()),
            None
        )

        if existente:
            # Actualizar precio y sumar cantidad
            existente["cantidad"] += nuevo["cantidad"]
            existente["precio"] = nuevo["precio"]
            fusionados += 1
        else:
            inventario_actual.append(nuevo)

    return fusionados
