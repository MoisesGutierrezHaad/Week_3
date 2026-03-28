"""
app.py - Punto de entrada principal del sistema de inventario.
Integra el menú interactivo y conecta los módulos servicios.py y archivos.py.
"""

from servicios import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    calcular_estadisticas
)
from archivos import guardar_csv, cargar_csv, fusionar_inventarios


def pedir_float(mensaje):
    """Solicita un número decimal no negativo al usuario."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("  El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("  Ingresa un número válido (ej: 12.5).")


def pedir_int(mensaje):
    """Solicita un número entero no negativo al usuario."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("  El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print(" Ingresa un número entero válido (ej: 10).")


def mostrar_menu():
    """Imprime el menú principal en consola."""
    print("\n" + "═" * 45)
    print("      SISTEMA DE INVENTARIO")
    print("═" * 45)
    print("  1. Agregar producto")
    print("  2. Mostrar inventario")
    print("  3. Buscar producto")
    print("  4. Actualizar producto")
    print("  5. Eliminar producto")
    print("  6. Ver estadísticas")
    print("  7. Guardar CSV")
    print("  8. Cargar CSV")
    print("  9. Salir")
    print("═" * 45)


def opcion_agregar(inventario):
    """Flujo para agregar un nuevo producto."""
    print("\n── AGREGAR PRODUCTO ──")
    nombre = input("  Nombre del producto: ").strip()
    if not nombre:
        print("  El nombre no puede estar vacío.")
        return
    precio = pedir_float("  Precio unitario: $")
    cantidad = pedir_int("  Cantidad en stock: ")
    agregar_producto(inventario, nombre, precio, cantidad)


def opcion_buscar(inventario):
    """Flujo para buscar un producto por nombre."""
    print("\n── BUSCAR PRODUCTO ──")
    nombre = input("  Nombre a buscar: ").strip()
    resultado = buscar_producto(inventario, nombre)
    if resultado:
        print(f"\n  Producto encontrado:")
        print(f"     Nombre  : {resultado['nombre']}")
        print(f"     Precio  : ${resultado['precio']:.2f}")
        print(f"     Cantidad: {resultado['cantidad']}")
    else:
        print(f"  Producto '{nombre}' no encontrado.")


def opcion_actualizar(inventario):
    """Flujo para actualizar precio y/o cantidad de un producto."""
    print("\n── ACTUALIZAR PRODUCTO ──")
    nombre = input("  Nombre del producto a actualizar: ").strip()

    if not buscar_producto(inventario, nombre):
        print(f"  Producto '{nombre}' no encontrado.")
        return

    print("  (Deja en blanco para no modificar ese campo)")

    # Precio
    entrada_precio = input("  Nuevo precio: $").strip()
    nuevo_precio = float(entrada_precio) if entrada_precio else None

    # Cantidad
    entrada_cantidad = input("  Nueva cantidad: ").strip()
    nueva_cantidad = int(entrada_cantidad) if entrada_cantidad else None

    if nuevo_precio is None and nueva_cantidad is None:
        print("  ℹNo se realizó ningún cambio.")
        return

    actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)


def opcion_eliminar(inventario):
    """Flujo para eliminar un producto con confirmación."""
    print("\n── ELIMINAR PRODUCTO ──")
    nombre = input("  Nombre del producto a eliminar: ").strip()

    if not buscar_producto(inventario, nombre):
        print(f"  Producto '{nombre}' no encontrado.")
        return

    confirmar = input(f"  ¿Confirmas eliminar '{nombre}'? (S/N): ").strip().upper()
    if confirmar == "S":
        eliminar_producto(inventario, nombre)
    else:
        print("  ℹ️  Eliminación cancelada.")


def opcion_estadisticas(inventario):
    """Flujo para mostrar estadísticas del inventario."""
    print("\n── ESTADÍSTICAS ──")
    stats = calcular_estadisticas(inventario)

    if not stats:
        print("  ℹEl inventario está vacío, no hay estadísticas.")
        return

    print(f" Unidades totales en stock : {stats['unidades_totales']}")
    print(f"  Valor total del inventario: ${stats['valor_total']:.2f}")
    print(f"  Producto más caro         : {stats['producto_mas_caro']['nombre']} "
          f"(${stats['producto_mas_caro']['precio']:.2f})")
    print(f"  Mayor stock               : {stats['producto_mayor_stock']['nombre']} "
          f"({stats['producto_mayor_stock']['cantidad']} unidades)")


def opcion_guardar(inventario):
    """Flujo para guardar el inventario en un CSV."""
    print("\n── GUARDAR CSV ──")
    ruta = input("  Ruta del archivo (ej: inventario.csv): ").strip()
    if not ruta:
        ruta = "inventario.csv"
    guardar_csv(inventario, ruta)


def opcion_cargar(inventario):
    """Flujo para cargar un CSV con opción de sobrescribir o fusionar."""
    print("\n── CARGAR CSV ──")
    ruta = input("  Ruta del archivo CSV a cargar: ").strip()

    resultado = cargar_csv(ruta)
    if resultado is None:
        return  # Error ya fue reportado dentro de cargar_csv

    productos_cargados, filas_invalidas = resultado

    if not productos_cargados:
        print("  No se encontraron productos válidos en el archivo.")
        if filas_invalidas:
            print(f"  {filas_invalidas} fila(s) inválida(s) omitida(s).")
        return

    # Preguntar al usuario: sobrescribir o fusionar
    print(f"\n  Se encontraron {len(productos_cargados)} producto(s) válidos.")
    decision = input("  ¿Sobrescribir inventario actual? (S/N): ").strip().upper()

    if decision == "S":
        # Reemplazar todo el inventario
        inventario.clear()
        inventario.extend(productos_cargados)
        accion = "Reemplazo total"
        print(f"  Inventario reemplazado con {len(productos_cargados)} producto(s).")
    else:
        # Fusionar con política definida
        fusionados = fusionar_inventarios(inventario, productos_cargados)
        accion = f"Fusión ({fusionados} actualizados, {len(productos_cargados) - fusionados} nuevos)"
        print(f"  Fusión completada.")

    # Resumen final
    print("\n  ── Resumen de carga ──")
    print(f"  Productos cargados : {len(productos_cargados)}")
    print(f"  Filas inválidas    : {filas_invalidas}")
    print(f"  Acción realizada   : {accion}")


# ─────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────
def main():
    inventario = []  # Lista de diccionarios: {"nombre", "precio", "cantidad"}

    print("\n  Bienvenido al Sistema de Inventario 🗃️")

    while True:
        mostrar_menu()

        try:
            opcion = int(input("  Selecciona una opción (1-9): "))
        except ValueError:
            print("  ⚠️  Ingresa un número entre 1 y 9.")
            continue

        if opcion == 1:
            opcion_agregar(inventario)
        elif opcion == 2:
            mostrar_inventario(inventario)
        elif opcion == 3:
            opcion_buscar(inventario)
        elif opcion == 4:
            opcion_actualizar(inventario)
        elif opcion == 5:
            opcion_eliminar(inventario)
        elif opcion == 6:
            opcion_estadisticas(inventario)
        elif opcion == 7:
            opcion_guardar(inventario)
        elif opcion == 8:
            opcion_cargar(inventario)
        elif opcion == 9:
            print("\n  👋 ¡Hasta luego!\n")
            break
        else:
            print("  ⚠️  Opción inválida. Elige entre 1 y 9.")


if __name__ == "__main__":
    main()
