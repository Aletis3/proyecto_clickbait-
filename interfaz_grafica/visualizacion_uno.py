# ===============================================================================
# INTERFAZ GRAFICA
# ===============================================================================

import os
import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime
from acciones.funciones import ejecutar_analisis, limpiar_todo
from analisis_manual.cargar_archivo_csv import cargar_y_analizar_csv
from acciones.cargar_imagen import cargar_y_analizar_imagen

# VENTANA PRINCIPAL
ventana_principal = tk.Tk()  # crea la ventana principal de la aplicación
ventana_principal.title("Proyecto Integrador - Alejandra Palomino")  # título de la ventana
ventana_principal.geometry("1050x480")       # tamaño fijo de la ventana (ancho x alto en píxeles)
ventana_principal.configure(bg="#F0F0F0")    # color de fondo gris claro
ventana_principal.resizable(False, False)    # no permite cambiar el tamaño de la ventana

# TÍTULO
titulo = tk.Label(
    ventana_principal,
    text="Análisis de titulares Clickbait",
    font=("Arial", 28, "bold"),
    bg="#F0F0F0",
    fg="#333333"
)
# agrega el título con espaciado vertical
titulo.pack(pady=(20, 10))

# CAMPO DE ENTRADA DE TEXTO Y BOTÓN "LIMPIAR"
# crea un marco (frame) dentro de la ventana principal con fondo gris claro,
# lo coloca en la parte superior y le añade un poco de espacio alrededor.
frame_entrada = tk.Frame(ventana_principal, bg="#F0F0F0")

frame_entrada.pack(fill="x", padx=110, pady=(20, 10))
etiqueta_titular = tk.Label(frame_entrada,
                            text="Ingrese un titular: ",
                            font=("Arial", 11),
                            bg="#F0F0F0",
                            fg="#333333")
etiqueta_titular.pack(side= "left")

# Botón "Limpiar" (borra el campo de texto y la tabla)
boton_limpiar = tk.Button(
    frame_entrada,
    text="Limpiar",
    width=8,
    font=("Arial",9),
    command=lambda: limpiar_todo(entrada_texto_usuario, tabla)
)
boton_limpiar.pack(side="right", padx=(5, 10), pady=(5, 10))

# Campo de texto donde el usuario escribe el titular a analizar
entrada_texto_usuario = tk.Text(frame_entrada, height=1, wrap="word", font=("Arial", 11))
entrada_texto_usuario.pack(side="left", fill="x", expand=True)

# BOTONES PRINCIPALES (ANALIZAR, CARGAR ARCHIVO, CARGAR IMAGEN)
frame_botones = tk.Frame(ventana_principal, bg="#F0F0F0")
frame_botones.pack(pady=(10, 20))

# Botón "Analizar" (ejecuta el análisis del titular ingresado)
boton_analizar = tk.Button(frame_botones,
                           text="Analizar",
                           width=15,
                           font=("Arial", 10))

# Botón "Cargar archivo" y "Cargar imagen"
boton_archivo = tk.Button(frame_botones,
                          text="Cargar archivo",
                          width=15,
                          font=("Arial", 10),
                          command=lambda: cargar_y_analizar_csv(entrada_texto_usuario, tabla)
                          )

boton_imagen = tk.Button(frame_botones,
                         text="Cargar imagen",
                         width=15,
                         font=("Arial", 10),
                         command=lambda: cargar_y_analizar_imagen(entrada_texto_usuario, tabla))

# Coloca los botones en la interfaz usando grid
boton_analizar.grid(row=0, column=0, padx=45)
boton_archivo.grid(row=0, column=1, padx=45)
boton_imagen.grid(row=0, column=2, padx=45)

# TABLA DE RESULTADOS CON 4 COLUMNAS
# Crea un marco (Frame) que contendrá la tabla y el scrollbar
panel_inferior = ttk.Frame(ventana_principal, relief="solid", borderwidth=1)
panel_inferior.pack(fill="x", padx=40, pady=(0, 8))

# Configura grid en panel_inferior
panel_inferior.grid_rowconfigure(0, weight=1)
panel_inferior.grid_columnconfigure(0, weight=1)

# Scrollbar vertical para la tabla
scroll_y = ttk.Scrollbar(panel_inferior, orient="vertical")
scroll_x = ttk.Scrollbar(panel_inferior, orient="horizontal")

# Configura la tabla (Treeview) con las columnas necesarias
tabla = ttk.Treeview(
    panel_inferior,
    columns=("Titular", "Analisis Manual", "Analisis Ai", "Coincidencia"),
    show="headings",
    height=9, # filas
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set)

# Define los encabezados de las columnas
tabla.heading("Titular", text="Titular")
tabla.heading("Analisis Manual", text="Análisis Manual")
tabla.heading("Analisis Ai", text="Análisis Ai")
tabla.heading("Coincidencia", text="Coincidencia")

# Ajusta el ancho de cada columna y su alineación
tabla.column("Titular", width=350)
tabla.column("Analisis Manual", width=90, anchor="center")
tabla.column("Analisis Ai", width=90, anchor="center")
tabla.column("Coincidencia", width=90, anchor="center")

# posicionar
tabla.grid(row=0, column=0, sticky="nsew")

scroll_x.grid(row=1, column=0, sticky="ew")

# Coloca la tabla en la fila 0 y columna 0,
# y hace que se expanda para llenar el espacio disponible
tabla.grid(row=0, column=0, sticky="nsew")

# Coloca la barra de desplazamiento horizontal
scroll_y.grid(row=0, column=1, sticky="ns")


# Configura colores para las filas según la etiqueta (tags)
tabla.tag_configure("coincide", background="lightgreen")    # Coincidencia Verdadero -> verde
tabla.tag_configure("no_coincide", background="lightcoral") # Coincidencia Falso -> rojo

# FUNCIÓN PARA EJECUTAR EL ANÁLISIS Y GUARDAR RESULTADOS EN JSON
# Toma el titular del campo de texto, ejecuta el análisis (manual + AI)
# Muestra el resultado en la tabla. Además, guarda el resultado en un archivo JSON.

def analizar_y_guardar():
    """
     Cuenta cantidad de filas antes del análisis para detectar si se agrega
    una nueva fila
    """
    filas_antes = len(tabla.get_children())

    # ejecuta el análisis usando la función importada (inserta la fila en la tabla)
    ejecutar_analisis(entrada_texto_usuario, tabla)

    # cuenta nuevamente las filas después de ejecutar el análisis
    filas_despues = len(tabla.get_children())

    # si no hay filas nuevas, significa que no se realizó un análisis (entrada vacía o error)
    if filas_despues <= filas_antes:
        return  # Salimos sin guardar nada

    # obtiene el identificador de la última fila insertada
    ultima_fila = tabla.get_children()[-1]

    # extrae los valores de esa última fila (Titular, Análisis Manual, Análisis AI, Coincidencia)
    valores = tabla.item(ultima_fila, "values")
    if not valores:
        return  # Si por alguna razón no hay valores, no continuamos

    # crea un diccionario con el resultado para guardar en JSON
    resultado = {
        "Titular": valores[0],
        "Análisis Manual": valores[1],
        "Análisis IA": valores[2],
        "Coincidencia": valores[3]
    }
    # verifica de que exista la carpeta de resultados JSON
    if not os.path.exists("resultados_json"):
        os.makedirs("resultados_json")

    # genera un nombre de archivo único usando la fecha y hora actual
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"resultado_{timestamp}.json"
    ruta_archivo = os.path.join("resultados_json", nombre_archivo)
    try:
        # guarda el diccionario de resultado en el archivo JSON (codificación UTF-8)
        with open(ruta_archivo, "w", encoding="utf-8") as fichero_json:
            json.dump(resultado, fichero_json, ensure_ascii=False, indent=4)
    except Exception as e:
        # si ocurre un error al guardar, informamos al usuario mediante un diálogo
        messagebox.showerror("Error al guardar", f"No se pudo guardar el resultado en JSON:\n{e}")

# asigna la función analizar_y_guardar al botón "Analizar"
boton_analizar.config(command=analizar_y_guardar)

# INICIAR LA APLICACIÓN (BUCLE PRINCIPAL DE TKINTER)
if __name__ == "__main__":
    ventana_principal.mainloop()
