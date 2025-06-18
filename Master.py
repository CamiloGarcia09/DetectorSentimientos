import streamlit as st
import os
import tempfile
from Cortar import cortar_audio
from Transcribir import transcribir_audio
from Traduccion import traducir_con_deepl
from Resumir import resumir_largo
from Sentimientos import analizar_sentimiento
import shutil

st.set_page_config(page_title="Análisis de Entrevistas", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #FFFFFF; font-size: 2.8em;'>🧠 Análisis Inteligente de Audio de Entrevistas</h1>
    <p style='text-align: center; font-size: 1.1em; color: #CFCFCF'>
        Sube tu archivo de audio, transcribe, resume y analiza emociones en segundos.
    </p>
""", unsafe_allow_html=True)

st.markdown("### 📤 Carga tu archivo:")
archivo = st.file_uploader("🔊 Elige un archivo .mp3 o .m4a", type=["mp3", "m4a"], label_visibility="collapsed")


if archivo:
    nombre_archivo = os.path.join(tempfile.gettempdir(), f"temp_audio.{archivo.name.split('.')[-1]}")
    with open(nombre_archivo, "wb") as f:
        f.write(archivo.read())

    with st.spinner("✂️ Cortando en segmentos de 8 minutos..."):
        carpeta_segmentos = cortar_audio(nombre_archivo, duracion_segmento_min=8)

    segmentos = sorted(os.listdir(carpeta_segmentos))

    st.markdown("### 🎧 Selecciona un segmento para analizar:")
    segmento_seleccionado = st.selectbox("", segmentos)

    if segmento_seleccionado and st.button("🚀 Procesar segmento"):
        ruta_segmento = os.path.join(carpeta_segmentos, segmento_seleccionado)

        with st.spinner("📝 Transcribiendo..."):
            texto_es = transcribir_audio(ruta_segmento)

        st.markdown("### 🗣️ Transcripción:")
        st.write(texto_es)
        st.divider()

        with st.spinner("🌐 Traduciendo al inglés..."):
            texto_en = traducir_con_deepl(texto_es, "EN-US")

        with st.spinner("🧾 Generando resumen..."):
            resumen_en = resumir_largo(texto_en)

        with st.spinner("🔁 Traduciendo resumen al español..."):
            resumen_es = traducir_con_deepl(resumen_en, "ES")

        st.markdown("### 📋 Resumen en Español:")
        st.write(resumen_es)
        st.divider()

        with st.spinner("🧠 Analizando sentimientos..."):
            parrafos = [p.strip() for p in resumen_es.strip().split("\n") if p.strip()]
            resultados = analizar_sentimiento(parrafos)

        st.markdown("### 🔍 Sentimientos por Párrafo:")
        def color_estrellas(label):
            if "5" in label:
                return f"🟢 `{label}`"
            elif "4" in label:
                return f"🟡 `{label}`"
            elif "3" in label:
                return f"🟠 `{label}`"
            else:
                    return f"🔴 `{label}`"

        for i, r in enumerate(resultados):
            st.markdown(f"**Párrafo {i+1}:** {r['parrafo']}")
            st.markdown(
                f"👉 Sentimiento: {color_estrellas(r['sentimiento'])} | "
                f"Confianza: `{r['confianza']}%`"
            )


        if st.button("🧹 Borrar archivos temporales"):
            try:
                shutil.rmtree(carpeta_segmentos)
                os.remove(nombre_archivo)
                st.success("✅ Archivos eliminados correctamente.")
            except Exception as e:
                st.error(f"❌ Error eliminando archivos: {e}")