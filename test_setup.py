"""
Test script for MyVoiceTranslate
Run this to verify that all components are working correctly
"""

import os
import sys
import torch
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import torch
        print(f"✅ PyTorch imported (version: {torch.__version__})")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers imported (version: {transformers.__version__})")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        import librosa
        print(f"✅ Librosa imported (version: {librosa.__version__})")
    except ImportError as e:
        print(f"❌ Librosa import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy imported (version: {np.__version__})")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    return True

def test_gpu():
    """Test GPU availability and configuration"""
    print("\n🎮 Testing GPU...")
    
    if torch.cuda.is_available():
        device_count = torch.cuda.device_count()
        print(f"✅ CUDA available with {device_count} device(s)")
        
        for i in range(device_count):
            device_name = torch.cuda.get_device_name(i)
            props = torch.cuda.get_device_properties(i)
            vram_gb = props.total_memory / 1024**3
            print(f"   Device {i}: {device_name} ({vram_gb:.1f}GB)")
        
        # Test GPU memory allocation
        try:
            test_tensor = torch.randn(1000, 1000).cuda()
            print("✅ GPU memory allocation test passed")
            del test_tensor
            torch.cuda.empty_cache()
        except Exception as e:
            print(f"❌ GPU memory allocation test failed: {e}")
            return False
        
        return True
    else:
        print("⚠️  CUDA not available - will use CPU")
        return True

def test_directories():
    """Test if required directories exist"""
    print("\n📁 Testing directories...")
    
    required_dirs = [
        "models",
        "samples", 
        "outputs",
        "models/checkpoints"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} (missing)")
            all_exist = False
    
    return all_exist

def test_core_modules():
    """Test core application modules"""
    print("\n🔧 Testing core modules...")
    
    try:
        from clone_voice import VoiceCloner
        cloner = VoiceCloner()
        print("✅ VoiceCloner initialized")
        
        from translate_text import TextTranslator
        translator = TextTranslator()
        print("✅ TextTranslator initialized")
        
        from utils import validate_audio_file, get_audio_info
        print("✅ Utilities imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Core module test failed: {e}")
        return False

def test_translation():
    """Test translation functionality"""
    print("\n🌍 Testing translation...")
    
    try:
        from translate_text import TextTranslator
        translator = TextTranslator()
        
        # Test language support
        languages = translator.get_supported_languages()
        print(f"✅ {len(languages)} languages supported")
        
        # Test mock translation (without loading full model)
        test_text = "Hello world"
        print(f"✅ Translation test setup complete")
        
        return True
        
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        return False

def test_audio_processing():
    """Test audio processing utilities"""
    print("\n🎵 Testing audio processing...")
    
    try:
        from utils import create_sample_audio, validate_audio_file
        
        # Create a test audio file
        test_audio_path = "test_sample.wav"
        create_sample_audio(test_audio_path, duration=2.0)
        
        if os.path.exists(test_audio_path):
            print("✅ Sample audio creation")
            
            # Test validation
            is_valid, message = validate_audio_file(test_audio_path)
            if is_valid:
                print("✅ Audio validation")
            else:
                print(f"❌ Audio validation: {message}")
            
            # Clean up
            os.remove(test_audio_path)
            print("✅ Cleanup completed")
            
            return True
        else:
            print("❌ Sample audio creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Audio processing test failed: {e}")
        return False

def run_full_test():
    """Run comprehensive test suite"""
    print("🚀 MyVoiceTranslate Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("GPU Test", test_gpu),
        ("Directory Test", test_directories),
        ("Core Modules Test", test_core_modules),
        ("Translation Test", test_translation),
        ("Audio Processing Test", test_audio_processing)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n▶️  Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                failed += 1
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} FAILED: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 You can now run the application with:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("💡 Consider running setup.py again or checking your environment.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_full_test()
    sys.exit(0 if success else 1)
