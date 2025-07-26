import streamlit as st
import os
import tempfile
import io
from pathlib import Path
import base64
from clone_voice import VoiceCloner, setup_openvoice_models
from translate_text import TextTranslator
from utils import validate_audio_file, get_audio_info, preprocess_voice_samples
import torch

# Page configuration
st.set_page_config(
    page_title="MyVoiceTranslate",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #ff7f0e;
    margin-bottom: 1rem;
}
.info-box {
    background-color: #f0f2f6;
    color: #262730;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
.success-box {
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
    border-left: 5px solid #28a745;
}
.error-box {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
    border-left: 5px solid #dc3545;
}
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'voice_cloner' not in st.session_state:
        st.session_state.voice_cloner = VoiceCloner()
    if 'translator' not in st.session_state:
        st.session_state.translator = TextTranslator()
    if 'speaker_trained' not in st.session_state:
        st.session_state.speaker_trained = False
    if 'models_loaded' not in st.session_state:
        st.session_state.models_loaded = False

def display_system_info():
    """Display system information in sidebar"""
    st.sidebar.markdown("### 🖥️ System Information")
    
    # GPU Information
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        st.sidebar.success(f"🚀 GPU: {gpu_name}")
        st.sidebar.info(f"💾 GPU Memory: {gpu_memory:.1f} GB")
        
        # Check if translator is using CPU fallback
        if hasattr(st.session_state, 'translator') and hasattr(st.session_state.translator, 'fallback_to_cpu'):
            if st.session_state.translator.fallback_to_cpu:
                st.sidebar.warning("⚠️ GPU incompatible - using CPU")
            else:
                st.sidebar.success("✅ GPU acceleration active")
    else:
        st.sidebar.warning("⚠️ No GPU detected - using CPU")
    
    # Model status
    st.sidebar.markdown("### 📦 Model Status")
    if st.session_state.models_loaded:
        st.sidebar.success("✅ Translation model loaded")
    else:
        st.sidebar.warning("⏳ Translation model not loaded")
    
    if st.session_state.speaker_trained:
        st.sidebar.success("✅ Voice model trained")
    else:
        st.sidebar.warning("⏳ Voice model not trained")

def load_models():
    """Load translation models"""
    if not st.session_state.models_loaded:
        with st.spinner("Loading translation models... This may take a few minutes."):
            success = st.session_state.translator.load_model()
            if success:
                st.session_state.models_loaded = True
                st.success("Translation model loaded successfully!")
            else:
                st.error("Failed to load translation model")
                return False
    return True

def voice_cloning_section():
    """Voice cloning section of the app"""
    st.markdown('<div class="sub-header">🎤 Voice Cloning</div>', unsafe_allow_html=True)
    
    # Check if speaker is already trained
    if st.session_state.voice_cloner.load_speaker_embedding():
        st.session_state.speaker_trained = True
        st.markdown('<div class="success-box">✅ Voice model is already trained and ready to use!</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Retrain Voice Model"):
            st.session_state.speaker_trained = False
            st.session_state.voice_cloner.speaker_embedding = None
            st.rerun()
        return True
    
    st.markdown("""
    <div class="info-box">
    📝 <b>Instructions:</b><br>
    1. Upload 3-5 audio samples of your voice (each 5-10 seconds)<br>
    2. Speak clearly and naturally<br>
    3. Use different sentences for better voice modeling<br>
    4. Supported formats: WAV, MP3, M4A
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Upload voice samples",
        type=['wav', 'mp3', 'm4a'],
        accept_multiple_files=True,
        help="Upload 3-5 clear voice samples, each 5-10 seconds long"
    )
    
    if uploaded_files:
        st.write(f"📁 Uploaded {len(uploaded_files)} files")
        
        # Display file information
        valid_files = []
        for i, uploaded_file in enumerate(uploaded_files):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.write(f"**File {i+1}:**")
            with col2:
                st.write(uploaded_file.name)
            with col3:
                # Save uploaded file temporarily for validation
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Validate file
                is_valid, message = validate_audio_file(temp_path)
                if is_valid:
                    st.success("✅")
                    valid_files.append(temp_path)
                else:
                    st.error("❌")
                    st.write(f"⚠️ {message}")
        
        # Train voice model button
        if len(valid_files) >= 2:
            if st.button("🎯 Train Voice Model", type="primary"):
                with st.spinner("Training voice model... This may take a few minutes."):
                    success = st.session_state.voice_cloner.extract_speaker_embedding(valid_files)
                    if success:
                        st.session_state.speaker_trained = True
                        st.success("🎉 Voice model trained successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to train voice model")
                
                # Clean up temp files
                for temp_file in valid_files:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
        else:
            st.warning("⚠️ Please upload at least 2 valid audio files to train the voice model")
    
    return st.session_state.speaker_trained

def translation_section():
    """Text translation and speech generation section"""
    st.markdown('<div class="sub-header">🌍 Translation & Speech Generation</div>', unsafe_allow_html=True)
    
    # Load models if not already loaded
    if not load_models():
        return
    
    # Text input
    input_text = st.text_area(
        "Enter text to translate and speak:",
        height=100,
        placeholder="Type your message here...",
        help="Enter the text you want to translate and convert to speech in your voice"
    )
    
    # Language selection
    col1, col2 = st.columns(2)
    
    with col1:
        source_language = st.selectbox(
            "Source Language:",
            options=st.session_state.translator.get_supported_languages(),
            index=0,  # Default to English
            help="Language of the input text"
        )
    
    with col2:
        target_language = st.selectbox(
            "Target Language:",
            options=st.session_state.translator.get_supported_languages(),
            index=1,  # Default to Spanish
            help="Language to translate to"
        )
    
    # Generate button
    if st.button("🎬 Generate Speech", type="primary", disabled=not input_text.strip()):
        if not st.session_state.speaker_trained:
            st.error("❌ Please train your voice model first!")
            return
        
        with st.spinner("Processing... Translating text and generating speech..."):
            # Step 1: Translate text
            translated_text = st.session_state.translator.translate_text(
                input_text, target_language, source_language
            )
            
            if translated_text:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.write(f"**Original ({source_language}):** {input_text}")
                st.write(f"**Translated ({target_language}):** {translated_text}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Step 2: Generate speech
                output_path = st.session_state.voice_cloner.generate_speech(
                    translated_text, 
                    st.session_state.translator.language_codes.get(target_language, 'en')
                )
                
                if output_path and os.path.exists(output_path):
                    st.success("🎉 Speech generated successfully!")
                    
                    # Audio player
                    with open(output_path, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format="audio/wav")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Audio",
                        data=audio_bytes,
                        file_name=f"translated_speech_{target_language.lower()}.wav",
                        mime="audio/wav"
                    )
                else:
                    st.error("❌ Failed to generate speech")
            else:
                st.error("❌ Failed to translate text")

def main():
    """Main application function"""
    # Initialize session state
    init_session_state()
    
    # Main header
    st.markdown('<div class="main-header">🎤 MyVoiceTranslate</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Multilingual Voice Cloning App (Offline)</p>', unsafe_allow_html=True)
    
    # Sidebar
    display_system_info()
    
    # About section in sidebar
    with st.sidebar.expander("ℹ️ About"):
        st.markdown("""
        **MyVoiceTranslate** uses AI to:
        - Clone your voice from samples
        - Translate text to different languages
        - Generate speech in your voice
        
        **Technologies:**
        - OpenVoice for voice cloning
        - M2M100 for translation
        - GPU acceleration with CUDA
        """)
    
    # Main content
    st.markdown("---")
    
    # Step 1: Voice Cloning
    voice_ready = voice_cloning_section()
    
    st.markdown("---")
    
    # Step 2: Translation and Speech Generation
    if voice_ready:
        translation_section()
    else:
        st.markdown('<div class="info-box">👆 Please complete voice cloning first before generating speech</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
    Built with ❤️ using Streamlit, OpenVoice, and M2M100<br>
    Running offline with GPU acceleration
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
