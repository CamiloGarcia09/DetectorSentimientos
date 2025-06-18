import os
import math
import tempfile
from pydub import AudioSegment
from imageio_ffmpeg import get_ffmpeg_exe 

AudioSegment.converter = get_ffmpeg_exe()
AudioSegment.ffprobe = get_ffmpeg_exe()

def cortar_audio(ruta_audio, duracion_segmento_min=8):
    audio = AudioSegment.from_file(ruta_audio)

    duracion_segmento = duracion_segmento_min * 60 * 1000  
    duracion_total = len(audio)
    partes = math.ceil(duracion_total / duracion_segmento)

    nombre_base = os.path.splitext(os.path.basename(ruta_audio))[0]
    carpeta_salida = os.path.join(tempfile.gettempdir(), f"{nombre_base}_segmentos")
    os.makedirs(carpeta_salida, exist_ok=True)

    for i in range(partes):
        inicio = i * duracion_segmento
        fin = min((i + 1) * duracion_segmento, duracion_total)
        segmento = audio[inicio:fin]
        salida = os.path.join(carpeta_salida, f"{nombre_base}_parte{i+1}.mp3")
        segmento.export(salida, format="mp3")

    return carpeta_salida
