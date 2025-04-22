
import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile
import os
import speech_recognition as sr

st.set_page_config(page_title="HOLA Traductor Móvil", page_icon="📱")

st.title("🗣️ Traductor con Voz - HOLA Mobile")
st.markdown("Hablá o escribí en cualquier idioma y escuchá la traducción.")

# Reconocimiento de voz
r = sr.Recognizer()
texto = ""

if st.button("🎙️ Hablar ahora"):
    with sr.Microphone() as source:
        st.info("Escuchando...")
        try:
            audio = r.listen(source, timeout=5)
            texto = r.recognize_google(audio)
            st.success(f"Texto detectado: {texto}")
        except sr.UnknownValueError:
            st.warning("No se entendió lo que dijiste.")
        except Exception as e:
            st.error(f"Error: {e}")

# Entrada manual alternativa
texto_input = st.text_area("✍️ O escribí el texto acá:", value=texto, height=100)

idioma_destino = st.selectbox(
    "🌐 Elegí el idioma destino:",
    ["en", "es", "fr", "pt", "it", "de", "ru", "zh-CN", "ja", "ko", "ar", "hi"],
    format_func=lambda x: {
        "en": "Inglés",
        "es": "Español",
        "fr": "Francés",
        "pt": "Portugués",
        "it": "Italiano",
        "de": "Alemán",
        "ru": "Ruso",
        "zh-CN": "Chino simplificado",
        "ja": "Japonés",
        "ko": "Coreano",
        "ar": "Árabe",
        "hi": "Hindi"
    }.get(x, x)
)

if st.button("🌈 Traducir y escuchar"):
    if texto_input.strip() == "":
        st.warning("Ingresá texto o hablá algo primero.")
    else:
        try:
            traduccion = GoogleTranslator(source='auto', target=idioma_destino).translate(texto_input)
            st.success("✅ Traducción:")
            st.markdown(f"**{traduccion}**")

            # Reproducir la voz de salida
            tts = gTTS(text=traduccion, lang=idioma_destino)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                st.audio(tmp_file.name, format="audio/mp3")
                os.unlink(tmp_file.name)
        except Exception as e:
            st.error(f"❌ Error: {e}")
