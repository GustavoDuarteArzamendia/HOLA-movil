import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile
import os
import speech_recognition as sr

st.set_page_config(page_title="HOLA Traductor Robusto", page_icon="🛡️")

st.title("🛡️ Traductor con Voz - Versión Robusta")
st.markdown("🎤 Hablá o escribí en cualquier idioma y escuchá la traducción con seguridad.")

try:
    r = sr.Recognizer()
    texto = ""

    if st.button("🎙️ Hablar ahora"):
        try:
            with sr.Microphone() as source:
                st.info("⏳ Escuchando...")
                audio = r.listen(source, timeout=6)
                texto = r.recognize_google(audio)
                st.success(f"📋 Texto detectado: {texto}")
        except sr.UnknownValueError:
            st.warning("⚠️ No se entendió lo que dijiste.")
        except sr.WaitTimeoutError:
            st.warning("⚠️ Tiempo de espera agotado. Intentá de nuevo.")
        except Exception as e:
            st.error(f"❌ Error en la entrada de voz: {e}")

    texto_input = st.text_area("✍️ O escribí tu mensaje:", value=texto, height=100)

    idioma_destino = st.selectbox(
        "🌍 Elegí idioma destino:",
        ["en", "es", "fr", "pt", "it", "de", "ru", "zh-CN", "ja", "ko", "ar", "hi"],
        format_func=lambda x: {
            "en": "Inglés", "es": "Español", "fr": "Francés", "pt": "Portugués",
            "it": "Italiano", "de": "Alemán", "ru": "Ruso", "zh-CN": "Chino",
            "ja": "Japonés", "ko": "Coreano", "ar": "Árabe", "hi": "Hindi"
        }.get(x, x)
    )

    if st.button("🌈 Traducir y reproducir"):
        if texto_input.strip() == "":
            st.warning("⚠️ No hay texto ingresado.")
        else:
            try:
                traduccion = GoogleTranslator(source='auto', target=idioma_destino).translate(texto_input)
                st.success("📝 Traducción exitosa:")
                st.markdown(f"**{traduccion}**")

                # Reproducir audio de traducción
                tts = gTTS(text=traduccion, lang=idioma_destino)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    st.audio(tmp.name, format="audio/mp3")
                    os.unlink(tmp.name)
            except Exception as e:
                st.error(f"❌ Error al traducir o generar audio: {e}")
except Exception as e:
    st.error(f"💥 Error general inesperado: {e}")