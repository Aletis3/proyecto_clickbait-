# ====================================================================
# FUNCIÓN DE ANÁLISIS MANUAL
# ====================================================================
import tkinter as tk
import json
import re
import google.generativeai as genai
from gemini.keys.api_key import API_KEY_GEMINI  # clave guardada en otro archivo

def mostrar_cartel_espera(mensaje="Analizando..."):
    ventana_espera = tk.Toplevel()
    ventana_espera.title("Por favor espere")
    ventana_espera.geometry("250x100")
    ventana_espera.resizable(False, False)
    etiqueta = tk.Label(ventana_espera, text=mensaje, font=("Arial", 12))
    etiqueta.pack(expand=True)
    ventana_espera.update()
    return ventana_espera

def analisis_manual(titular: str):
    # crea cartel de espera
    ventana_espera = mostrar_cartel_espera()
    # define listas con palabras y números típicos del clickbait
    palabras_clickbait = ["último momento", "confirmado", "increíble", "te hará rico",
                          "científicos dicen", "no podrás creer", "sorprendente",
                          "impactante", "viral", "secreto", "truco", "hack",
                          "revelado", "exclusivo", "bomba", "escándalo", "shock"]
    numeros_clickbait = ["5", "10", "7", "3", "15"]

    # inicia el puntaje en cero
    puntaje = 0

    # cuenta cantidad de letras mayúsculas en el titular
    cantidad_mayusculas = 0
    for letra in titular:
        if letra.isupper():
            cantidad_mayusculas += 1

    # si hay más de 5 mayúsculas suma un punto
    if cantidad_mayusculas > 5:
        puntaje += 1

    # cuenta los signos de exclamación '!'
    cantidad_exclamaciones = titular.count("!")
    puntaje += cantidad_exclamaciones  # sumamos un punto por cada exclamación

    # revisa si hay palabras comunes de clickbait en el titular
    for palabra in palabras_clickbait:
        if palabra in titular.lower():
            puntaje += 2  # cada palabra clickbait suma 2 puntos

    # revisa números "típicos" de titulares clickbait en el titular
    for numero in numeros_clickbait:
        if numero in titular:
            puntaje += 1  # cada número típico suma 1 punto

    # decide si titular es 'clickbait' o 'confiable' según el puntaje
    if puntaje > 3:
        resultado = "Clickbait"
    else:
        resultado = "Confiable"

    return resultado, puntaje

# ====================================================================
# FUNCIÓN ANALISIS IA - RESPUESTAS
# ====================================================================

def analizar_titular_json(titular: str):
    """
    Analiza un titular de noticia usando análisis manual y la IA de Gemini,
    y devuelve un resultado en formato JSON.
    Posibles categorías de la IA: "CONFIABLE" o "DUDOSO CLICKBAIT".
    """

    # verifica que el titular no esté vacío
    if not titular or not titular.strip():
        return "Error: No se ingresó ningún titular."

    # verifica que la clave de API de Gemini exista
    if not API_KEY_GEMINI:
        return "Error: No se encontró la API key de Gemini."

    # configura la conexion cona la IA usando la clave API
    genai.configure(api_key=API_KEY_GEMINI)

    # elege el modelo de Gemini
    model = genai.GenerativeModel("gemini-2.5-flash")

    # crea el prompt que se enviará a la IA de Gemini
    prompt = f"""
Analizá el siguiente titular de noticia y clasificá su nivel de confiabilidad.

Criterios:
- Si tiene palabras exageradas, muchas mayúsculas o signos de exclamación, puede ser "DUDOSO CLICKBAIT".
- Si parece una noticia normal, objetiva y de fuente confiable, es "CONFIABLE".

Respondé estrictamente en este formato JSON:
{{
  "Evaluación Ai": "Confiable" o "Dudoso Clickbait"
  
}}

Titular: "{titular}"
""".strip()

        # llama a la IA de Gemini
    response = model.generate_content(prompt)

    try:
        # Realiza el análisis manual del titular.
        # Nos devuelve una tupla: resultado y puntaje, pero el resultado se ignora.
        # Usa "_" para ignorar el puntaje.
        resultado_manual, _ = analisis_manual(titular) # Ignora el puntaje númerico con ' _'


        # extre el texto de la respuesta devuelta por Gemini
        texto = ""
        if hasattr(response, "text") and response.text:
            texto = response.text.strip()
        if not texto:
            # si hay texto en la respuesta, se genera un error
            raise ValueError("Gemini no devolvió texto de respuesta.")

        # intenta convertir la respuesta en un objeto JSON
        try:
            datos_ai = json.loads(texto)
            valor = datos_ai.get("Evaluación Ai") or datos_ai.get("Evaluacion Ai")
        except Exception:
            valor = None

        # si el archivo JSON no tenía el formato esperado, busca el valor con una expresiónes regulares
        if not valor:
            m = re.search(r'"Evaluaci[oó]n\s*Ai"\s*:\s*"([^"]+)"', texto, flags=re.IGNORECASE)
            if m:
                valor = m.group(1)

            # si todavía no encuentra el valor, busca palabras clave en el texto
            if not valor:
                if "confiable" in texto.lower():
                    valor = "Confiable"
                elif "dudoso" in texto.lower() or "clickbait" in texto.lower():
                    valor = "Dudoso Clickbait"
                else:
                    valor = "No identificado"

        # guarda la evaluación de la IA
        resultado_ia = valor

        # compara el resultado con el de la IA para determinar la coincidencia
        if (resultado_manual == "Confiable" and resultado_ia == "Confiable") or \
           (resultado_manual == "Clickbait" and resultado_ia == "Dudoso Clickbait"):
            coincidencia = "Verdadero"
        else:
            coincidencia = "Falso"      # No coinciden las evaluaciones

        # prepara los datos finales con todos los campos requeridos
        datos = {
            "Titular": titular,
            "Análisis Manual": resultado_manual,
            "Análisis Ai": resultado_ia,
            "Coincidencia": coincidencia
        }
        # convierte el diccionario a un formato JSON y lo devuelve
        return json.dumps(datos, ensure_ascii=False, indent=2)

    except Exception as e:
        # si ocurre cualquier error al usar Gemini, devuelve un mensaje de error
        raise RuntimeError(f"❌ Error al usar Gemini: {e}")
