#====================================================================
# CONFIGURACIÓN DE TESSERACT
#====================================================================
# Usar Tesseract para leer texto de una imagen procesada
import pytesseract


def leer_texto(imagen_preparada):
    if imagen_preparada is None:
        return ""

    # oem 3 --> la red neuronal encargada de reconocer los caracteres
    # psm 6 --> page segmentation mode -->como segmenta el texto  (4 varios parrafos // 7 para una sola linea)
    # preservar los espacios correctos de la imagen
    # agregar caracteres a la lista de permitidos


    configuracion = "--oem 3  --psm  6  -l spa"


    try:
        texto = pytesseract.image_to_string(imagen_preparada, config=configuracion)

        # elimina espacios sobrantes, saltos de línea y tabulaciones, dejando solo un espacio entre palabras
        texto_limpio = " ".join(texto.split())
        # devuelve el texto sin espacios al inicio ni al final
        return  texto_limpio

    except Exception as e:
        # si ocurre un error durante la extracción de texto,
        # muestra un mensaje de error y devuelve una cadena vacía
        print(f"[ERROR Tesseract]: {e}")
        return ""

