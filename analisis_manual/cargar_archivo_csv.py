# ===============================================================================
# CARGAR Y ANALIZAR ARCHIVO CSV
# ===============================================================================

# Este archivo sirve para cargar un archivo CSV y analizar sus titulares.
# Solo se pueden cargar archivos .csv que tengan una columna que se llame "titular".

import pandas as pd  # pandas sirve para leer archivos como Excel o CSV
from tkinter import filedialog, messagebox  # Para abrir la ventana de "Buscar archivo"
from analisis_manual.evaluacion_manual_gemini import analizar_titular_json  # Tu función de análisis
import json  # Para guardar los resultados en formato JSON
import os  # Para crear carpetas si no existen


def cargar_y_analizar_csv(entrada_texto_usuario, tabla):

    # abre la ventana para elegir un archivo
    # solo muestra archivos .csv
    ruta = filedialog.askopenfilename(
        title="Elige un archivo CSV",
        filetypes=[("Archivos CSV", "*.csv")] )

    # si el usuario no elige ningún archivo, la función termina
    if not ruta:
        return

    try:
        # lee el archivo csv usando codificación utf-8 y separador ";"
        # usa encoding="utf-8" para que lea tildes y ñ
        # usa sep=";" porque el CSV usa punto y coma
        datos = pd.read_csv(ruta, encoding="utf-8", sep=";")

        # verifica que exista la columna "titular"
        if "titular" not in datos.columns:
            messagebox.showerror("Error", "El archivo debe tener una columna llamada 'titular'.")
            return

        # obtiene la lista de titulares, elimina valores vacíos y los convierte en lista
        lista_titulares = datos["titular"].dropna().tolist()

        # si no hay titulares en la lista, muestra una advertencia y termina
        if len(lista_titulares) == 0:
            messagebox.showwarning("Advertencia", "El archivo no tiene titulares.")
            return

        # crea la carpeta "resultados_json" si aún no existe
        if not os.path.exists("resultados_json"):
            os.makedirs("resultados_json")

        # define ruta de archivo donde se guardarán los resultados
        archivo_resultados = "resultados_json/resultados.json"

        # carga resultados anteriores (si existen)
        try:
            with open(archivo_resultados, "r", encoding="utf-8") as f:
                todos_los_resultados = json.load(f)
        except:
        # si no existe o está vacío, empezamos con una lista vacía
            todos_los_resultados = []

        # recorre cada titular de la lista para analizarlo
        for titular in lista_titulares:
            # convierte el titular a texto por si estuviese en otro formato
            titular = str(titular)

        # analiza el titular usando la función que combina reglas manuales e IA
            resultado_en_json = analizar_titular_json(titular)

        # convierte los resultados en formato json, a un diccionario de Python
            resultado = json.loads(resultado_en_json)

        # extrae los campos necesarios para el resultado
            texto_titular = resultado["Titular"]
            analisis_manual = resultado["Análisis Manual"]
            analisis_ia = resultado["Análisis Ai"]
            coincidencia = resultado["Coincidencia"]

        # define el color de la fila
            if coincidencia == "Verdadero":
                color = ("coincide",)
            else:
                color = ("no_coincide",)

        # agrega una nueva fila a la tabla con los resultados de análisis
            tabla.insert("", "end", values=(texto_titular, analisis_manual, analisis_ia, coincidencia), tags=color)

        # añade el resultado actual a la lista general de este resultado
            todos_los_resultados.append(resultado)

        # guarda todos los resultados en el archivo JSON
        with open(archivo_resultados, "w", encoding="utf-8") as f:
            json.dump(todos_los_resultados, f, ensure_ascii=False, indent=2)

        # muestra un mensaje indicando que el análisis terminó correctamente
        messagebox.showinfo("Listo", f"Se analizaron {len(lista_titulares)} titulares.")

    except Exception as error:
        # si ocurre algún error durante el proceso, muestra un mensaje
        messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{error}")