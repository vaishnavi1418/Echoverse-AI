import streamlit as st

# Page settings
st.set_page_config(page_title="EchoVerse", layout="wide")

# Title & Description
st.title("🎧 EchoVerse")
st.markdown(
    """
    Transform your text into expressive audiobooks. ✨ 
    Rewrite tone with **IBM Watsonx Granite** and generate natural-sounding narration via **IBM Watson Text-to-Speech**.
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
    voice = st.selectbox("Voice", ["Lisa", "Michael", "Allison"])
    rewrite_btn = st.button("✍️ Rewrite Tone")

st.markdown("---")

# Audio Section
st.header("🔊 Audio")

playback_speed = st.slider("Playback speed", 0.5, 2.0, 1.0, 0.1)

col3, col4 = st.columns([1, 2])
with col3:
    generate_btn = st.button("🎶 Generate Audio")

with col4:
    st.info("Your audio will appear here after generation.")
    # Example placeholder audio
    # st.audio("sample.mp3", format="audio/mp3")
    # st.download_button("⬇️ Download Audio", data=open("sample.mp3","rb"), file_name="output.mp3")

st.markdown("---")

# Comparison Section
st.header("📊 Side-by-Side Comparison")
col5, col6 = st.columns(2)

with col5:
    st.subheader("Original")
    st.text_area("Original Text", value=input_text, height=200, key="orig_text")

with col6:
    st.subheader(f"Rewritten ({tone})")
    st.text_area("Rewritten Text", value="", height=200, key="rewritten_text")
