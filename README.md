# proyecto_clickbait
Análisis de titulares Clickbait - Proyecto Integrador
<p align="center">
  <img src="https://raw.githubusercontent.com/Aletis3/proyecto_clickbait-/main/images/foto_banner.png" width="1000"/>
</p>

## Descripción

Este proyecto fue desarrollado en el marco de las asignaturas **Proyecto Integrador** y **Técnicas de Procesamiento de Imágenes**.  
Su propósito es analizar titulares de noticias y detectar posibles características de *clickbait* mediante dos enfoques:

- **Análisis manual**, basado en criterios lingüísticos definidos por el usuario.  
- **Análisis con IA**, utilizando el modelo **Gemini** de Google Generative AI.  

El sistema está programado en **Python** y cuenta con una **interfaz gráfica (Tkinter)** que facilita la interacción con los usuarios.
Además, incluye un módulo de **procesamiento de imágenes** que permite analizar titulares presentes en capturas o fotografías de noticias.  
Mediante las librerías **OpenCV** y **Pytesseract**, el sistema realiza un reconocimiento óptico de caracteres (OCR) para extraer el texto y evaluarlo con los mismos criterios del análisis manual y de IA.


**Estructura de la carpeta de entrega:**  
- `proyecto_integrador/` → Contiene el código principal del sistema. Incluye los módulos de análisis, procesamiento de imágenes y la interfaz gráfica.  
- `archivos_de_prueba/` → Reúne archivos CSV e imágenes de ejemplo para realizar pruebas de funcionamiento.  

**Instrucciones de uso:**  
1. Ejecutar el archivo principal de la interfaz: `visualizacion_uno.py`.  
2. Cargar un archivo CSV o escribir un titular manualmente.  
3. Observar el resultado del análisis manual y el generado por la IA.  
4. Guardar los resultados en formato JSON para futuras consultas o comparaciones.  

**Seguridad y privacidad:**  
La clave API de Gemini se encuentra protegida localmente en la carpeta `gemini/` y está excluida del repositorio mediante el archivo `.gitignore`.

**Autora:** Alejandra Palomino — **Año:** 2025


## Carpeta de la interfaz gráfica
Contiene los archivos principales del entorno **Tkinter** del proyecto, encargados de la visualización, interacción con el usuario y ejecución de las funciones de análisis.
[interfaz_grafica](interfaz_grafica)


## ⚙️ Instalación

### Clonar el repositorio
```bash
git clone https://github.com/Aleti3/proyecto_clickbait-.git
cd proyecto_clickbait-
```
### Instalar dependencias
``` bash
pip install -r requirements.txt
```
Este comando instalará automáticamente todas las librerías necesarias para ejecutar el proyecto.
