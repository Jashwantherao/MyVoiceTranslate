import os
import librosa
import soundfile as sf
import numpy as np
from pydub import AudioSegment
from typing import Union, Tuple
import tempfile

def convert_audio_format(input_path: str, output_path: str, target_format: str = "wav") -> bool:
    """Convert audio file to target format"""
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=target_format)
        return True
    except Exception as e:
        print(f"Error converting audio format: {str(e)}")
        return False

def normalize_audio(audio_path: str, target_db: float = -20.0) -> str:
    """Normalize audio to target dB level"""
    try:
        audio = AudioSegment.from_file(audio_path)
        
        # Calculate current dB level
        current_db = audio.dBFS
        
        # Calculate gain needed
        gain_needed = target_db - current_db
        
        # Apply gain
        normalized_audio = audio + gain_needed
        
        # Save normalized audio
        output_path = audio_path.replace('.wav', '_normalized.wav')
        normalized_audio.export(output_path, format="wav")
        
        return output_path
    except Exception as e:
        print(f"Error normalizing audio: {str(e)}")
        return audio_path

def trim_silence(audio_path: str, top_db: int = 20) -> str:
    """Remove silence from beginning and end of audio"""
    try:
        # Load audio with librosa
        audio, sr = librosa.load(audio_path, sr=None)
        
        # Trim silence
        trimmed_audio, _ = librosa.effects.trim(audio, top_db=top_db)
        
        # Save trimmed audio
        output_path = audio_path.replace('.wav', '_trimmed.wav')
        sf.write(output_path, trimmed_audio, sr)
        
        return output_path
    except Exception as e:
        print(f"Error trimming silence: {str(e)}")
        return audio_path

def split_audio_by_duration(audio_path: str, max_duration: float = 10.0) -> list:
    """Split audio into chunks of maximum duration"""
    try:
        audio = AudioSegment.from_file(audio_path)
        duration = len(audio) / 1000.0  # Convert to seconds
        
        if duration <= max_duration:
            return [audio_path]
        
        chunks = []
        chunk_duration_ms = int(max_duration * 1000)
        
        for i in range(0, len(audio), chunk_duration_ms):
            chunk = audio[i:i + chunk_duration_ms]
            chunk_path = audio_path.replace('.wav', f'_chunk_{i//chunk_duration_ms}.wav')
            chunk.export(chunk_path, format="wav")
            chunks.append(chunk_path)
        
        return chunks
    except Exception as e:
        print(f"Error splitting audio: {str(e)}")
        return [audio_path]

def validate_audio_file(audio_path: str) -> Tuple[bool, str]:
    """Validate audio file and return status with message"""
    try:
        if not os.path.exists(audio_path):
            return False, "File does not exist"
        
        # Try to load with librosa
        audio, sr = librosa.load(audio_path, sr=None)
        
        if len(audio) == 0:
            return False, "Audio file is empty"
        
        duration = len(audio) / sr
        if duration < 1.0:
            return False, f"Audio too short: {duration:.2f}s (minimum 1s required)"
        
        if duration > 30.0:
            return False, f"Audio too long: {duration:.2f}s (maximum 30s recommended)"
        
        return True, f"Valid audio file: {duration:.2f}s at {sr}Hz"
        
    except Exception as e:
        return False, f"Error validating audio: {str(e)}"

def get_audio_info(audio_path: str) -> dict:
    """Get detailed information about audio file"""
    try:
        audio, sr = librosa.load(audio_path, sr=None)
        duration = len(audio) / sr
        
        return {
            'path': audio_path,
            'duration': duration,
            'sample_rate': sr,
            'channels': 1 if len(audio.shape) == 1 else audio.shape[1],
            'samples': len(audio),
            'format': os.path.splitext(audio_path)[1],
            'size_mb': os.path.getsize(audio_path) / (1024 * 1024)
        }
    except Exception as e:
        return {'error': str(e)}

def preprocess_voice_samples(sample_paths: list, output_dir: str = "samples/processed") -> list:
    """Preprocess multiple voice samples for training"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        processed_paths = []
        
        for i, sample_path in enumerate(sample_paths):
            if not os.path.exists(sample_path):
                print(f"Warning: Sample {sample_path} not found, skipping...")
                continue
            
            # Validate audio
            is_valid, message = validate_audio_file(sample_path)
            if not is_valid:
                print(f"Warning: {sample_path} - {message}")
                continue
            
            # Process audio
            processed_path = os.path.join(output_dir, f"processed_sample_{i}.wav")
            
            # Convert to standard format
            if not convert_audio_format(sample_path, processed_path, "wav"):
                continue
            
            # Normalize
            normalized_path = normalize_audio(processed_path)
            
            # Trim silence
            trimmed_path = trim_silence(normalized_path)
            
            # Final processed file
            final_path = os.path.join(output_dir, f"final_sample_{i}.wav")
            os.rename(trimmed_path, final_path)
            
            # Clean up intermediate files
            for temp_file in [processed_path, normalized_path]:
                if os.path.exists(temp_file) and temp_file != final_path:
                    os.remove(temp_file)
            
            processed_paths.append(final_path)
            print(f"Processed sample {i+1}/{len(sample_paths)}: {final_path}")
        
        return processed_paths
        
    except Exception as e:
        print(f"Error preprocessing voice samples: {str(e)}")
        return []

def create_sample_audio(output_path: str, duration: float = 5.0, sample_rate: int = 24000):
    """Create a sample audio file for testing purposes"""
    try:
        # Generate a simple tone
        t = np.linspace(0, duration, int(sample_rate * duration))
        frequency = 440  # A4 note
        audio = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Add some variation
        audio += 0.1 * np.sin(2 * np.pi * 880 * t)  # Harmonic
        audio += 0.05 * np.random.randn(len(audio))  # Noise
        
        # Apply envelope
        envelope = np.exp(-t / (duration * 0.3))
        audio = audio * envelope
        
        # Save audio
        sf.write(output_path, audio, sample_rate)
        print(f"Sample audio created: {output_path}")
        
    except Exception as e:
        print(f"Error creating sample audio: {str(e)}")

if __name__ == "__main__":
    # Test utilities
    print("Testing audio utilities...")
    
    # Create test samples directory
    os.makedirs("samples", exist_ok=True)
    
    # Create sample audio files for testing
    for i in range(3):
        create_sample_audio(f"samples/test_sample_{i}.wav", duration=3.0 + i)
    
    # Test preprocessing
    sample_files = [f"samples/test_sample_{i}.wav" for i in range(3)]
    processed = preprocess_voice_samples(sample_files)
    
    print(f"Processed {len(processed)} samples successfully")
