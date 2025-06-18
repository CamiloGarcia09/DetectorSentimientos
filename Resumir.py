from transformers import pipeline
from Traduccion import traducir_con_deepl

resumidor = pipeline("summarization", model="facebook/bart-large-cnn")

def resumir_largo(texto, max_chunk=1000):

    partes = [texto[i:i + max_chunk] for i in range(0, len(texto), max_chunk)]
    resumen_final = ""

    for parte in partes:
        resumen = resumidor(parte, max_length=120, min_length=30, do_sample=False)
        resumen_final += resumen[0]['summary_text'] + "\n\n"

    return resumen_final.strip()

def resumen_traducido(texto_es):

    texto_en = traducir_con_deepl(texto_es, "EN-US")
    resumen_en = resumir_largo(texto_en)
    resumen_es = traducir_con_deepl(resumen_en, "ES")
    return resumen_es
