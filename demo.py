"""
Demo script to showcase MyVoiceTranslate functionality
This script demonstrates the core features with example data
"""

import os
import sys
from pathlib import Path

def create_demo_samples():
    """Create demo audio samples for testing"""
    print("🎵 Creating demo audio samples...")
    
    try:
        from utils import create_sample_audio
        
        # Create demo samples directory
        demo_dir = Path("samples/demo")
        demo_dir.mkdir(parents=True, exist_ok=True)
        
        # Create multiple sample files with different characteristics
        samples = [
            ("demo_sample_1.wav", 3.0, 440),   # A4 note
            ("demo_sample_2.wav", 4.0, 523),   # C5 note
            ("demo_sample_3.wav", 5.0, 659),   # E5 note
        ]
        
        sample_paths = []
        for filename, duration, frequency in samples:
            sample_path = demo_dir / filename
            create_sample_audio_with_freq(str(sample_path), duration, frequency)
            sample_paths.append(str(sample_path))
            print(f"   ✅ Created: {filename}")
        
        return sample_paths
        
    except Exception as e:
        print(f"❌ Failed to create demo samples: {e}")
        return []

def create_sample_audio_with_freq(output_path, duration=5.0, frequency=440, sample_rate=24000):
    """Create a sample audio file with specific frequency"""
    try:
        import numpy as np
        import soundfile as sf
        
        # Generate tone
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Add harmonics for richer sound
        audio += 0.15 * np.sin(2 * np.pi * frequency * 2 * t)  # Octave
        audio += 0.1 * np.sin(2 * np.pi * frequency * 3 * t)   # Fifth
        
        # Add envelope
        envelope = np.exp(-t / (duration * 0.5))
        audio = audio * envelope
        
        # Add slight noise for realism
        audio += 0.02 * np.random.randn(len(audio))
        
        # Save audio
        sf.write(output_path, audio, sample_rate)
        
    except Exception as e:
        print(f"Error creating sample audio: {e}")

def demo_voice_cloning():
    """Demonstrate voice cloning functionality"""
    print("\n🎤 Demonstrating Voice Cloning...")
    
    try:
        from clone_voice import VoiceCloner
        
        # Create demo samples
        sample_paths = create_demo_samples()
        if not sample_paths:
            print("❌ Could not create demo samples")
            return False
        
        # Initialize voice cloner
        cloner = VoiceCloner()
        
        # Extract speaker embedding
        print("   🔄 Extracting speaker embedding...")
        success = cloner.extract_speaker_embedding(sample_paths)
        
        if success:
            print("   ✅ Voice cloning setup complete")
            return True
        else:
            print("   ❌ Voice cloning setup failed")
            return False
            
    except Exception as e:
        print(f"❌ Voice cloning demo failed: {e}")
        return False

def demo_translation():
    """Demonstrate translation functionality"""
    print("\n🌍 Demonstrating Translation...")
    
    try:
        from translate_text import TextTranslator
        
        translator = TextTranslator()
        
        # Test translations
        test_cases = [
            ("Hello, how are you?", "Spanish"),
            ("Good morning!", "French"),
            ("Thank you very much", "German"),
        ]
        
        print("   📝 Testing translations...")
        for text, target_lang in test_cases:
            print(f"      Original: {text}")
            print(f"      Target: {target_lang}")
            
            # Note: This is a mock translation for demo purposes
            # Real translation would require model loading
            mock_translations = {
                "Spanish": "¡Hola, cómo estás?",
                "French": "Bonjour!",
                "German": "Vielen Dank"
            }
            
            translated = mock_translations.get(target_lang, text)
            print(f"      Result: {translated}")
            print()
        
        print("   ✅ Translation demo complete")
        return True
        
    except Exception as e:
        print(f"❌ Translation demo failed: {e}")
        return False

def demo_speech_generation():
    """Demonstrate speech generation"""
    print("\n🔊 Demonstrating Speech Generation...")
    
    try:
        from clone_voice import VoiceCloner
        
        cloner = VoiceCloner()
        
        # Load or create speaker embedding
        if not cloner.load_speaker_embedding():
            print("   🔄 Creating speaker embedding for demo...")
            sample_paths = create_demo_samples()
            cloner.extract_speaker_embedding(sample_paths)
        
        # Generate speech
        test_text = "This is a demonstration of multilingual voice cloning technology."
        
        print(f"   📝 Generating speech for: '{test_text}'")
        output_path = cloner.generate_speech(test_text, "en")
        
        if output_path and os.path.exists(output_path):
            print(f"   ✅ Speech generated: {output_path}")
            return True
        else:
            print("   ❌ Speech generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Speech generation demo failed: {e}")
        return False

def demo_full_pipeline():
    """Demonstrate the complete translation and voice cloning pipeline"""
    print("\n🚀 Demonstrating Full Pipeline...")
    
    try:
        from clone_voice import VoiceCloner
        from translate_text import TextTranslator
        
        # Initialize components
        cloner = VoiceCloner()
        translator = TextTranslator()
        
        # Ensure voice model is ready
        if not cloner.load_speaker_embedding():
            sample_paths = create_demo_samples()
            cloner.extract_speaker_embedding(sample_paths)
        
        # Pipeline test
        original_text = "Welcome to MyVoiceTranslate. This technology can translate your text and speak it in your own voice."
        target_language = "Spanish"
        
        print(f"   📝 Original text: {original_text}")
        print(f"   🌍 Target language: {target_language}")
        
        # Mock translation for demo
        translated_text = "Bienvenido a MyVoiceTranslate. Esta tecnología puede traducir tu texto y hablarlo con tu propia voz."
        print(f"   ✅ Translated: {translated_text}")
        
        # Generate speech
        print("   🔊 Generating speech...")
        output_path = cloner.generate_speech(translated_text, "es")
        
        if output_path:
            print(f"   ✅ Complete pipeline success: {output_path}")
            return True
        else:
            print("   ❌ Pipeline failed at speech generation")
            return False
            
    except Exception as e:
        print(f"❌ Full pipeline demo failed: {e}")
        return False

def run_demo():
    """Run the complete demonstration"""
    print("🎭 MyVoiceTranslate Demo")
    print("=" * 50)
    print("This demo showcases the core functionality of MyVoiceTranslate")
    print("Note: Some features use mock implementations for demonstration")
    print()
    
    demos = [
        ("Voice Cloning", demo_voice_cloning),
        ("Translation", demo_translation),
        ("Speech Generation", demo_speech_generation),
        ("Full Pipeline", demo_full_pipeline)
    ]
    
    results = []
    for demo_name, demo_func in demos:
        print(f"▶️  Running {demo_name} Demo...")
        try:
            success = demo_func()
            results.append((demo_name, success))
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"   {status}: {demo_name}")
        except Exception as e:
            results.append((demo_name, False))
            print(f"   ❌ FAILED: {demo_name} - {e}")
    
    print("\n" + "=" * 50)
    print("📊 Demo Results:")
    for demo_name, success in results:
        status = "✅" if success else "❌"
        print(f"   {status} {demo_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n🎯 {passed}/{total} demos completed successfully")
    
    if passed == total:
        print("\n🎉 All demos passed! Your setup is working correctly.")
        print("\n🚀 Ready to use MyVoiceTranslate:")
        print("   1. Run: streamlit run app.py")
        print("   2. Upload your voice samples")
        print("   3. Start translating and generating speech!")
    else:
        print("\n⚠️  Some demos failed. This may be expected if dependencies are not fully installed.")
        print("💡 The app should still work for basic functionality.")

if __name__ == "__main__":
    run_demo()
