#!/usr/bin/env python3
"""
Setup script for MyVoiceTranslate
This script helps set up the environment and download required models
"""

import os
import sys
import subprocess
import platform
import torch
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ is required. Current version:", f"{version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_cuda():
    """Check CUDA availability"""
    if torch.cuda.is_available():
        cuda_version = torch.version.cuda
        device_count = torch.cuda.device_count()
        device_name = torch.cuda.get_device_name(0) if device_count > 0 else "Unknown"
        print(f"✅ CUDA available: {cuda_version}")
        print(f"✅ GPU Device: {device_name}")
        print(f"✅ GPU Count: {device_count}")
        
        # Check VRAM
        if device_count > 0:
            vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✅ GPU Memory: {vram_gb:.1f} GB")
            if vram_gb < 8:
                print("⚠️  Warning: Less than 8GB VRAM detected. Performance may be limited.")
        return True
    else:
        print("⚠️  CUDA not available. CPU will be used (slower performance)")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "models",
        "models/translation",
        "models/checkpoints", 
        "samples",
        "samples/processed",
        "outputs"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {dir_path}")

def install_requirements():
    """Install Python requirements"""
    try:
        print("📦 Installing Python requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_openvoice():
    """Setup OpenVoice (placeholder - requires manual setup)"""
    print("🎤 Setting up OpenVoice...")
    print("📋 OpenVoice requires manual installation:")
    print()
    print("   Option 1 - Automated (Windows):")
    print("   .\\install_openvoice.bat")
    print()
    print("   Option 2 - Manual:")
    print("   1. git clone https://github.com/myshell-ai/OpenVoice.git")
    print("   2. cd OpenVoice")
    print("   3. pip install -e .")
    print("   4. Download required checkpoints (see OpenVoice docs)")
    print()
    print("   Option 3 - Use Mock Mode:")
    print("   The app will work with simulated voice cloning for testing")
    print("   Set mock_voice_cloning = False in config.py when ready")
    print()
    print("⚠️  For now, mock voice cloning is enabled for immediate testing")

def test_installation():
    """Test if installation is working"""
    try:
        print("🧪 Testing installation...")
        
        # Test imports with more detailed error reporting
        packages_to_test = [
            ('streamlit', 'Streamlit'),
            ('torch', 'PyTorch'),
            ('transformers', 'Hugging Face Transformers'),
            ('librosa', 'Librosa'),
            ('numpy', 'NumPy'),
            ('soundfile', 'SoundFile'),
            ('pydub', 'PyDub')
        ]
        
        failed_imports = []
        
        for package, name in packages_to_test:
            try:
                __import__(package)
                print(f"✅ {name} imported successfully")
            except ImportError as e:
                print(f"❌ {name} import failed: {e}")
                failed_imports.append(name)
        
        if failed_imports:
            print(f"\n⚠️  Some packages failed to import: {', '.join(failed_imports)}")
            print("The app may still work with reduced functionality.")
        
        # Test basic functionality
        try:
            from clone_voice import VoiceCloner
            from translate_text import TextTranslator
            
            cloner = VoiceCloner()
            translator = TextTranslator()
            
            print("✅ Core modules loaded successfully")
            return len(failed_imports) == 0
            
        except Exception as e:
            print(f"❌ Core modules test failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 MyVoiceTranslate Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    print("\n🖥️  System Information:")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.architecture()[0]}")
    
    # Check CUDA
    print("\n🎮 GPU Information:")
    cuda_available = check_cuda()
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    if not install_requirements():
        print("❌ Installation failed. Please check error messages above.")
        sys.exit(1)
    
    # Setup OpenVoice
    print("\n🎤 Voice Cloning Setup:")
    setup_openvoice()
    
    # Test installation
    print("\n🧪 Testing installation...")
    test_success = test_installation()
    
    if test_success:
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 You can now run the application with:")
        print("   streamlit run app.py")
        print("\n📚 Next steps:")
        print("   1. Complete OpenVoice setup (run .\\install_openvoice.bat)")
        print("   2. Upload voice samples and test the app")
        print("   3. For now, mock voice cloning is enabled")
        print("\n💡 The app is ready to use with basic functionality!")
    else:
        print("\n⚠️  Setup completed with some issues.")
        print("The app should still work with reduced functionality.")
        print("\n🚀 You can try running the application with:")
        print("   streamlit run app.py")
        print("\n🔧 To resolve issues, check the error messages above.")

if __name__ == "__main__":
    main()
