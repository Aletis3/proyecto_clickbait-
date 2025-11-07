# ======================================================================
# PREPROCESADO DE IMAGEN (cv2)
# ======================================================================
import cv2
import numpy as np
#import matplotlib.pyplot as plt

def mostrar_imagen(imagen_preparada):
    """Muestra la imagen preprocesada en una ventana separada (no en PyCharm)."""
    # redimensionar para que no sea demasiado grande
    alto, ancho = imagen_preparada.shape
    escala = min(800 / ancho, 600 / alto, 1.0)  # máximo 800x600
    ancho_nuevo = int(ancho * escala)
    alto_nuevo = int(alto * escala)
    imagen_pequena = cv2.resize(imagen_preparada, (ancho_nuevo, alto_nuevo), interpolation=cv2.INTER_AREA)

    # Mostrar en ventana de OpenCV
    cv2.imshow("Imagen preprocesada para OCR", imagen_pequena)
    cv2.waitKey(0)  # Espera a que pulses una tecla
    cv2.destroyAllWindows()  # Cierra la ventana


    # # Muestra la imagen preprocesada en una ventana.
    # # Convertir de BGR (OpenCV) a RGB (matplotlib)
    # img_rgb = cv2.cvtColor(imagen_preparada, cv2.COLOR_GRAY2RGB)
    # plt.imshow(img_rgb)
    # plt.axis('off')
    # plt.title("Imagen preprocesada para OCR")
    # plt.show()


def preparar_imagen (ruta_imagen):
    # carga y preprocesa una imagen para mejorar el OCR.
    # leer la imagen
    imagen = cv2.imread(ruta_imagen)

    if imagen is None:
        raise FileNotFoundError(f"No se puede abrir la imagen: {ruta_imagen}")
    print("La imagen se cargó correctamente")

    # convertir a escala de grises
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # aumentar resolución
    escala = 2.0
    alto, ancho = gray.shape
    gray = cv2.resize(gray, (int(ancho * escala), int(alto * escala)), interpolation=cv2.INTER_CUBIC)

    # suavizar
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # binarizar con Otsu
    _, binaria = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # afinar letras
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    afinada = cv2.erode(binaria, kernel, iterations=1)

    # invertir si está muy oscura
    if np.mean(afinada) < 127:
        afinada = cv2.bitwise_not(afinada)

    return afinada


