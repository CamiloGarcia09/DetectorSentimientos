import os
import math
import tempfile
import subprocess

def cortar_audio(ruta_audio, duracion_segmento_min=8):
    duracion_segmento = duracion_segmento_min * 60
    nombre_base = os.path.splitext(os.path.basename(ruta_audio))[0]
    carpeta_salida = os.path.join(tempfile.gettempdir(), f"{nombre_base}_segmentos")
    os.makedirs(carpeta_salida, exist_ok=True)


    cmd_duracion = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", ruta_audio
    ]
    duracion_total = float(subprocess.check_output(cmd_duracion).strip())
    partes = math.ceil(duracion_total / duracion_segmento)

    for i in range(partes):
        inicio = i * duracion_segmento
        salida = os.path.join(carpeta_salida, f"{nombre_base}_parte{i+1}.mp3")

        cmd_corte = [
            "ffmpeg", "-i", ruta_audio, "-ss", str(inicio), "-t", str(duracion_segmento),
            "-acodec", "copy", salida, "-y"
        ]
        subprocess.run(cmd_corte, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return carpeta_salida
