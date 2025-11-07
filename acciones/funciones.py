# ======================================================================
# GESTOR DE ANÁLISIS
# ======================================================================
import json
from tkinter import messagebox
import os
from analisis_manual.evaluacion_manual_gemini import analizar_titular_json

def ejecutar_analisis(entrada_texto_usuario, tabla):
    """
    Realiza el análisis de un titular ingresado por el usuario (manual + IA),
    muestra los resultados en la tabla con colores según coincidencia,
    Limpia el campo de entrada, guarda el resultado en un archivo JSON acumulativo
    muestra un mensaje de confirmación.
    """

    # obtiene el texto escrito por el usuario en el cuadro de entrada
    titular = entrada_texto_usuario.get("1.0", "end").strip()

    # si el cuadro de texto está vacío, advierte al usuario y sale sin analizar
    if not titular:
        messagebox.showwarning("Aviso", "Por favor, escribí un titular para analizar.")
        return

    try:
        # ejecuta el análisis combinado (manual + IA) que nos devuelve un JSON (en formato str)
        json_str = analizar_titular_json(titular)

        # convierte el texto JSON obtenido a un diccionario de Python para usar sus datos
        datos = json.loads(json_str)

        # extrae los valores necesarios del diccionario
        # si alguna clave no existe, usa cadena vacia.
        t = datos.get("Titular", "")
        manu = datos.get("Análisis Manual", "")
        ai = datos.get("Análisis Ai", "")
        coin = datos.get("Coincidencia", "")

        # define el estilo visual según el valor de Coincidencia, definimos el color (tag) de la fila en la tabla
        if coin == "Verdadero":
            tag = ("coincide",)    # Coincidencia verdadera -> fondo verde
        elif coin == "Falso":
            tag = ("no_coincide",)  # Coincidencia falsa -> fondo rojo
        else:
            tag = ()  # Sin color especial en otros casos (por ejemplo, errores)

        # agrega una nueva fila a la tabla con los valores obtenidos
        tabla.insert("", "end", values=(t, manu, ai, coin), tags=tag)

        # limpia el cuadro de entrada para que quede listo para el siguiente titular
        entrada_texto_usuario.delete("1.0", "end")
        entrada_texto_usuario.focus_set()

# ======================================================================
# GUARDADo DEL RESULTADO EN ARCHIVO JSON
# ======================================================================

        # crea la carpeta 'resultados_json' si aún no existe
        # permite almacenar un historial acumulado de todos los análisis realizados.
        folder = "resultados_json"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # define la ruta del archivo json donde se guardan todos los análisis
        file_path = os.path.join(folder, "resultados.json")

        # carga los resultados anteriores si el archivo no existe
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    resultados_previos = json.load(f)
                except json.JSONDecodeError:
                    resultados_previos = []  # archivo estaba vacío o corrupto, inicia lista nueva
        else:
             resultados_previos = []  # primer análisis: lista vacía

        # agrega el nuevo resultado al historial
        resultados_previos.append(datos)

        # guarda toda la lista actualizada en el archivo json, con formato legible y soporte para tildes
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(resultados_previos, f, ensure_ascii=False, indent=2)

        # mensaje opcional de éxito para el usuario
        messagebox.showinfo("Listo", "El titular fue analizado correctamente.")

    except Exception as e:
        # si ocurre cualquier error (por ejemplo, falla la conexión con la ia),
        # se informa al usuario con un mensaje de error detallado
        messagebox.showerror("Error",
                             f"Ocurrió un problema al analizar el titular:\n\n{e}")


def ejecutar_titular(entrada_texto_usuario, tabla):
    """
    Alias para mantener compatibilidad con código anterior.
    Hace exactamente lo mismo que ejecutar_analisis(...).
    """
    ejecutar_analisis(entrada_texto_usuario, tabla)

def limpiar_todo(entrada, tabla):
    """
    Limpia el cuadro de entrada y todas las filas de la tabla.
    """
    # Limpiamos el texto del cuadro de entrada
    try:
        entrada.delete("1.0", "end")
        entrada.focus_set()
    except Exception:
        pass  # Ignoramos cualquier error inesperado al borrar

    # Borramos todas las filas de la tabla de resultados
    try:
        for fila in tabla.get_children():
            tabla.delete(fila)
    except Exception:
        pass
