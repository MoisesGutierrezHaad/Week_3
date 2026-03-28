"""
servicios.py - Módulo con operaciones CRUD y estadísticas del inventario.
"""


def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto.
        precio (float): Precio unitario (debe ser >= 0).
        cantidad (int): Cantidad en stock (debe ser >= 0).

    Retorna:
        bool: True si se agregó, False si el producto ya existe.
    """
    # Verificar si el producto ya existe (búsqueda insensible a mayúsculas)
    if buscar_producto(inventario, nombre):
        print(f"   El producto '{nombre}' ya existe. Usa 'Actualizar' para modificarlo.")
        return False

    inventario.append({
        "nombre": nombre,
        "precio": float(precio),
        "cantidad": int(cantidad)
    })
    print(f"  Producto '{nombre}' agregado correctamente.")
    return True


def mostrar_inventario(inventario):
    """
    Imprime todos los productos del inventario en formato tabla.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.

    Retorna:
        None
    """
    if not inventario:
        print("  ℹ El inventario está vacío.")
        return

    # Encabezado de la tabla
    print("\n  " + "─" * 52)
    print(f"  {'NOMBRE':<20} {'PRECIO':>10} {'CANTIDAD':>10}  SUBTOTAL")
    print("  " + "─" * 52)

    subtotal = lambda p: p["precio"] * p["cantidad"]  # (Opcional) lambda para subtotal

    for producto in inventario:
        print(
            f"  {producto['nombre']:<20} "
            f"${producto['precio']:>9.2f} "
            f"{producto['cantidad']:>10} "
            f"  ${subtotal(producto):>9.2f}"
        )

    print("  " + "─" * 52)
    print(f"  Total de productos en lista: {len(inventario)}\n")


def buscar_producto(inventario, nombre):
    """
    Busca un producto en el inventario por nombre (sin distinguir mayúsculas).

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto a buscar.

    Retorna:
        dict | None: El diccionario del producto si se encuentra, None si no existe.
    """
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza el precio y/o cantidad de un producto existente.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto a actualizar.
        nuevo_precio (float, opcional): Nuevo precio. Si es None, no se cambia.
        nueva_cantidad (int, opcional): Nueva cantidad. Si es None, no se cambia.

    Retorna:
        bool: True si se actualizó, False si el producto no existe.
    """
    producto = buscar_producto(inventario, nombre)

    if not producto:
        print(f"  ⚠️  Producto '{nombre}' no encontrado.")
        return False

    # Solo actualizar los campos proporcionados
    if nuevo_precio is not None:
        producto["precio"] = float(nuevo_precio)
    if nueva_cantidad is not None:
        producto["cantidad"] = int(nueva_cantidad)

    print(f"  Producto '{nombre}' actualizado correctamente.")
    return True


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.
        nombre (str): Nombre del producto a eliminar.

    Retorna:
        bool: True si se eliminó, False si no se encontró.
    """
    producto = buscar_producto(inventario, nombre)

    if not producto:
        print(f"   Producto '{nombre}' no encontrado.")
        return False

    inventario.remove(producto)
    print(f"  Producto '{nombre}' eliminado.")
    return True


def calcular_estadisticas(inventario):
    """
    Calcula métricas generales del inventario.

    Parámetros:
        inventario (list): Lista de diccionarios con los productos.

    Retorna:
        dict: Diccionario con las métricas:
              - unidades_totales (int)
              - valor_total (float)
              - producto_mas_caro (dict con nombre y precio)
              - producto_mayor_stock (dict con nombre y cantidad)
        None: Si el inventario está vacío.
    """
    if not inventario:
        return None

    subtotal = lambda p: p["precio"] * p["cantidad"]

    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)

    # Producto con mayor precio y mayor stock
    producto_mas_caro = max(inventario, key=lambda p: p["precio"])
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": {
            "nombre": producto_mas_caro["nombre"],
            "precio": producto_mas_caro["precio"]
        },
        "producto_mayor_stock": {
            "nombre": producto_mayor_stock["nombre"],
            "cantidad": producto_mayor_stock["cantidad"]
        }
    }
