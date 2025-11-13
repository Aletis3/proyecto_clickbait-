# ===============================================================================
# FUNCION PARA CARGAR, PREPROCESAR Y ANALIZAR UNA IMAGEN
# ===============================================================================

from tkinter import filedialog, messagebox
from procesamiento_de_imagenes.arreglo_de_imagenes import preparar_imagen, mostrar_imagen
from procesamiento_de_imagenes.tesseract_configuracion import leer_texto
from acciones.funciones import ejecutar_analisis
import tkinter as tk


def cargar_y_analizar_imagen(entrada_texto_usuario, tabla):
    """
      Permite al usuario seleccionar una imagen, extraer su texto y analizarlo
      como si fuera un titular ingresado manualmente.
      """
    # abre cuadro de diálogo para elegir imagen
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg") ] )

    if not ruta:
        return

    try:
        # preprocesa la imagen para mejorar la calidad
        imagen_procesada = preparar_imagen(ruta) # función en arreglo_de_imagenes

        # muestra mensaje informativo al usuario
        messagebox.showinfo(
            "Atención",
            "Se mostrará la imagen procesada.\n\n"
            "Por favor, ciérrela para que comience el análisis.")

        # muestra imagen preprocesada
        mostrar_imagen(imagen_procesada)

        # extrae texto de la imagen
        texto_extraido = leer_texto(imagen_procesada) # tesseract_configuracion

        # si no se detecta texti, avisa al ususario y termina
        if not texto_extraido:
            messagebox.showwarning("Sin texto", "No se encontró texto en la imagen.")
            return

        # limpia el texto extraído, elimina saltos de líneas y espacios
        texto_limpio = " ".join(texto_extraido.split())

        # coloca el texto limpio en el cuadro de entrada
        entrada_texto_usuario.delete("1.0", "end")
        # inserta el texto extraído
        entrada_texto_usuario.insert("1.0",
                                     texto_limpio)

        # ejecuta el análsis del titular, igual que con el texto ingresado
        ejecutar_analisis(entrada_texto_usuario, tabla)

    except Exception as e:
        # si ocurre cualquier error (imagen dañada, OCR fallido, etc.),
        # se muestra un mensaje de error al usuario
        messagebox.showerror("Error", f"No se pudo procesar la imagen:\n{e}")