import whisper

model = whisper.load_model("base")

def transcribir_audio(ruta_audio):

    try:
        resultado = model.transcribe(ruta_audio)
        return resultado["text"]
    except Exception as e:
        print(f"❌ Error al transcribir: {e}")
        return ""
