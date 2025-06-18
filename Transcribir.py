import whisper

model = whisper.load_model("base")

def transcribir_audio(ruta_audio):
    """
    Transcribe un archivo de audio usando el modelo Whisper.
    
    Parámetros:
    ruta_audio (str): Ruta al archivo de audio (.mp3, .wav, etc.)

    Retorna:
    str: Texto transcrito
    """
    try:
        resultado = model.transcribe(ruta_audio)
        return resultado["text"]
    except Exception as e:
        print(f"❌ Error al transcribir: {e}")
        return ""
