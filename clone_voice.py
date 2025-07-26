import os
import torch
import librosa
import soundfile as sf
import numpy as np
from typing import List, Tuple
import tempfile
from pathlib import Path

class VoiceCloner:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.fallback_to_cpu = False
        self.speaker_embedding = None
        self.checkpoints_dir = Path("models/checkpoints")
        self.checkpoints_dir.mkdir(exist_ok=True)
        
    def preprocess_audio(self, audio_path: str, target_sr: int = 24000) -> np.ndarray:
        """Preprocess audio file for voice cloning"""
        try:
            # Load audio
            audio, sr = librosa.load(audio_path, sr=None)
            
            # Resample if necessary
            if sr != target_sr:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
            
            # Normalize audio
            audio = audio / np.max(np.abs(audio))
            
            # Remove silence
            audio, _ = librosa.effects.trim(audio, top_db=20)
            
            return audio
        except Exception as e:
            raise Exception(f"Error preprocessing audio {audio_path}: {str(e)}")
    
    def extract_speaker_embedding(self, audio_samples: List[str]) -> bool:
        """Extract speaker embedding from multiple audio samples"""
        try:
            # For now, we'll create a mock speaker embedding
            # In a real implementation, you would use OpenVoice here
            processed_audios = []
            
            for sample_path in audio_samples:
                if os.path.exists(sample_path):
                    audio = self.preprocess_audio(sample_path)
                    processed_audios.append(audio)
                else:
                    print(f"Warning: Audio sample {sample_path} not found")
            
            if not processed_audios:
                raise Exception("No valid audio samples found")
            
            # Create a mock speaker embedding (in real implementation, use OpenVoice)
            self.speaker_embedding = {
                'embedding': np.random.rand(256),  # Mock embedding
                'sample_rate': 24000,
                'num_samples': len(processed_audios)
            }
            
            # Save speaker embedding
            embedding_path = self.checkpoints_dir / "speaker_embedding.npy"
            np.save(embedding_path, self.speaker_embedding)
            
            print(f"Speaker embedding extracted from {len(processed_audios)} samples")
            return True
            
        except Exception as e:
            print(f"Error extracting speaker embedding: {str(e)}")
            return False
    
    def load_speaker_embedding(self) -> bool:
        """Load previously saved speaker embedding"""
        try:
            embedding_path = self.checkpoints_dir / "speaker_embedding.npy"
            if embedding_path.exists():
                self.speaker_embedding = np.load(embedding_path, allow_pickle=True).item()
                print("Speaker embedding loaded successfully")
                return True
            else:
                print("No saved speaker embedding found")
                return False
        except Exception as e:
            print(f"Error loading speaker embedding: {str(e)}")
            return False
    
    def generate_speech(self, text: str, language: str = "en", output_path: str = None) -> str:
        """Generate speech using cloned voice"""
        try:
            if self.speaker_embedding is None:
                raise Exception("No speaker embedding available. Please clone voice first.")
            
            # Mock TTS generation (in real implementation, use OpenVoice TTS)
            # Generate a simple sine wave as placeholder
            duration = len(text) * 0.1  # Rough estimation
            sample_rate = 24000
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 440 + np.random.randn() * 50  # Random pitch variation
            audio = 0.3 * np.sin(2 * np.pi * frequency * t)
            
            # Add some variation to make it sound more natural
            noise = 0.05 * np.random.randn(len(audio))
            audio = audio + noise
            
            # Apply speaker characteristics (mock)
            audio = audio * (1 + 0.1 * np.sin(2 * np.pi * 2 * t))
            
            if output_path is None:
                output_path = f"outputs/generated_speech_{language}_{hash(text) % 10000}.wav"
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "outputs", exist_ok=True)
            
            # Save audio
            sf.write(output_path, audio, sample_rate)
            
            print(f"Speech generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            return None
    
    def clone_and_generate(self, voice_samples: List[str], text: str, language: str = "en") -> str:
        """Complete pipeline: clone voice and generate speech"""
        try:
            # Extract speaker embedding if not already done
            if self.speaker_embedding is None:
                success = self.extract_speaker_embedding(voice_samples)
                if not success:
                    return None
            
            # Generate speech
            output_path = self.generate_speech(text, language)
            return output_path
            
        except Exception as e:
            print(f"Error in clone_and_generate: {str(e)}")
            return None

# Utility functions for OpenVoice integration (placeholder)
def setup_openvoice_models():
    """Download and setup OpenVoice models"""
    try:
        # In a real implementation, download OpenVoice models here
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        print("OpenVoice models setup completed (mock)")
        return True
    except Exception as e:
        print(f"Error setting up OpenVoice models: {str(e)}")
        return False

if __name__ == "__main__":
    # Test the voice cloner
    cloner = VoiceCloner()
    
    # Setup models
    setup_openvoice_models()
    
    # Test with sample audio files (if they exist)
    sample_files = ["samples/sample1.wav", "samples/sample2.wav"]
    if any(os.path.exists(f) for f in sample_files):
        result = cloner.clone_and_generate(sample_files, "Hello, this is a test of voice cloning technology.", "en")
        if result:
            print(f"Generated speech saved to: {result}")
    else:
        print("No sample audio files found for testing")
