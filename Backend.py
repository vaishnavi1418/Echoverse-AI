import streamlit as st
from transformers import pipeline, AutoProcessor, AutoModelForSpeechSeq2Seq
import tempfile

# --------------------------
# Load Hugging Face Models
# --------------------------

# (1) Text rewriting placeholder: using Granite speech model as base (not ideal for TTS, but demo purpose)
processor = AutoProcessor.from_pretrained("ibm-granite/granite-speech-3.3-2b")
model = AutoModelForSpeechSeq2Seq.from_pretrained("ibm-granite/granite-speech-3.3-2b")

# (2) Text-to-Speech pipeline (use an open-source TTS model)
tts = pipeline("text-to-speech", model="facebook/mms-tts-eng")  # replace with Watson API in production

# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(page_title="EchoVerse", layout="wide")
st.title("🎧 EchoVerse")
st.markdown(
    """
    Transform your text into expressive audiobooks. ✨  
    Rewrite tone with **IBM Watsonx Granite** and generate natural-sounding narration via **Text-to-Speech**.
    """
)

st.markdown("---")

# Input Section
st.header("📖 Input Text")

col1, col2 = st.columns([2, 1])

with col1:
    input_text = st.text_area("Paste text", height=150, placeholder="Paste or type your text here...")
    uploaded_file = st.file_uploader("Upload .txt file", type=["txt"])
    if uploaded_file:
        input_text = uploaded_file.read().decode("utf-8")

with col2:
    tone = st.selectbox("Tone", ["Neutral", "Suspenseful", "Inspiring"])
    voice = st.selectbox("Voice", ["Lisa", "Michael", "Allison"])  # placeholder for IBM Watson voices
    rewrite_btn = st.button("✍️ Rewrite Tone")

# Tone rewriting simulation (placeholder)
rewritten_text = ""
if rewrite_btn and input_text:
    # Just append tone marker (real implementation would use LLM for style transfer)
    rewritten_text = f"[{tone} tone] {input_text}"
    st.success("✅ Text rewritten successfully!")

st.markdown("---")

# Audio Section
st.header("🔊 Audio")

playback_speed = st.slider("Playback speed", 0.5, 2.0, 1.0, 0.1)
col3, col4 = st.columns([1, 2])

with col3:
    generate_btn = st.button("🎶 Generate Audio")

with col4:
    if generate_btn and (rewritten_text or input_text):
        text_for_audio = rewritten_text if rewritten_text else input_text

        with st.spinner("Generating audio... 🎤"):
            # Run TTS
            tts_output = tts(text_for_audio)

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(tts_output["audio"])
                audio_path = tmp.name

            # Playback + download
            st.audio(audio_path, format="audio/wav")
            with open(audio_path, "rb") as f:
                st.download_button("⬇️ Download Audio", data=f, file_name="echoverse_output.wav")

st.markdown("---")

# Comparison Section
st.header("📊 Side-by-Side Comparison")
col5, col6 = st.columns(2)

with col5:
    st.subheader("Original")
    st.text_area("Original Text", value=input_text, height=200, key="orig_text")

with col6:
    st.subheader(f"Rewritten ({tone})")
    st.text_area("Rewritten Text", value=rewritten_text, height=200, key="rewritten_text")
