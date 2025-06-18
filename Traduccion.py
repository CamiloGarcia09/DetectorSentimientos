import deepl
import os

DEEPL_API_KEY = "257035c1-89b2-4b0c-8f9f-3c023b9de344:fx"

translator = deepl.Translator(DEEPL_API_KEY)

def traducir_con_deepl(texto, destino="EN-US"):
    """
    Traduce un texto al idioma destino usando la API de DeepL.

    Parámetros:
    texto (str): Texto original
    destino (str): Código del idioma destino (ej: "EN-US", "ES")

    Retorna:
    str: Texto traducido
    """
    try:
        resultado = translator.translate_text(texto, target_lang=destino)
        return resultado.text
    except Exception as e:
        print(f"❌ Error al traducir: {e}")
        return texto
