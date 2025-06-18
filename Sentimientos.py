from transformers import pipeline

analizador = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analizar_sentimiento(parrafos):
    """
    Analiza una lista de párrafos y devuelve una lista de resultados con sentimiento y score.
    """
    resultados = analizador(parrafos)
    analisis = []
    for i, resultado in enumerate(resultados):
        analisis.append({
            "parrafo": parrafos[i],
            "sentimiento": resultado["label"],
            "confianza": round(resultado["score"] * 100, 2)
        })
    return analisis
