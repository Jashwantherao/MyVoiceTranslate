# 🔧 MyVoiceTranslate Troubleshooting Guide

## Common Installation Issues

### 1. **OpenVoice Package Not Found**
**Error:** `ERROR: No matching distribution found for openvoice`

**Solution:**
- This is expected! OpenVoice is not on PyPI
- Run the fixed setup: `.\setup.bat` (already updated)
- Install OpenVoice separately: `.\install_openvoice.bat`
- Or use mock mode for testing (enabled by default)

### 2. **Python Version Compatibility**
**Error:** `Requires-Python <3.12,>=3.8`

**Solution:**
- Some packages don't support Python 3.12+ yet
- Use Python 3.10 or 3.11 for best compatibility
- Download from: https://www.python.org/downloads/

### 3. **CUDA/GPU Issues**
**Error:** CUDA not detected or memory errors

**Solutions:**
- Install CUDA 11.8 or 12.x from NVIDIA
- Update GPU drivers
- For testing, the app works on CPU (slower)
- Close other GPU applications

### 4. **Audio Dependencies**
**Error:** `pydub` or `librosa` import errors

**Solutions:**
- Install ffmpeg: `winget install ffmpeg` (Windows 11)
- Or download from: https://ffmpeg.org/
- Some audio formats may not work without ffmpeg

### 5. **Virtual Environment Issues**
**Error:** Virtual environment activation fails

**Solutions:**
```powershell
# Delete and recreate
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Quick Fixes

### Reset Installation
```powershell
# Clean reset
rmdir /s venv
del /q models\*
.\setup.bat
```

### Test Without GPU
Edit `config.py`:
```python
GPU_CONFIG = {
    'use_gpu': False,  # Changed from True
    # ... rest unchanged
}
```

### Use CPU-only PyTorch
```powershell
pip uninstall torch torchaudio
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Mock Mode Only
Edit `config.py`:
```python
DEV_CONFIG = {
    'mock_voice_cloning': True,  # Keep enabled
    # ... rest unchanged
}
```

## Verification Steps

### 1. Test Basic Setup
```powershell
python test_setup.py
```

### 2. Test Demo
```powershell
python demo.py
```

### 3. Launch App
```powershell
streamlit run app.py
```

### 4. Check Dependencies
```powershell
pip list | findstr torch
pip list | findstr streamlit
pip list | findstr transformers
```

## Platform-Specific Notes

### Windows 10/11
- Use Windows PowerShell (not Command Prompt)
- Install Visual C++ Build Tools if needed
- Windows Defender may slow down installation

### Windows 11 with winget
```powershell
winget install Python.Python.3.11
winget install Git.Git
winget install Gyan.FFmpeg
```

### Antivirus Software
- Exclude the project folder from real-time scanning
- Some antivirus software blocks model downloads

## Getting Help

### Debug Information
```powershell
python --version
pip --version
nvidia-smi  # Check GPU
where python
where pip
```

### Log Files
Check these locations for errors:
- Terminal output during setup
- Windows Event Viewer
- `%TEMP%\pip-*` folders

### Community Support
- GitHub Issues: Create detailed bug reports
- Include system info and error messages
- Mention if you're using mock mode or real OpenVoice

## Success Indicators

✅ **Setup Successful:**
- Virtual environment created
- All core packages installed
- Streamlit starts without errors
- GPU detected (optional)

✅ **App Working:**
- Web interface loads at http://localhost:8501
- Can upload audio files
- Translation works (even with mock voice)
- Audio playback functions

## Performance Tips

### Faster Installation
```powershell
# Use faster pip mirror
pip install -r requirements.txt -i https://pypi.douban.com/simple/
```

### Reduce Memory Usage
Edit `config.py`:
```python
MODEL_CONFIG = {
    'batch_size': 1,  # Reduce if needed
    'max_sequence_length': 256,  # Reduce from 512
}
```

### Skip Optional Features
Use `requirements_minimal.txt`:
```powershell
pip install -r requirements_minimal.txt
```

---

**Remember:** The app works in mock mode for immediate testing. OpenVoice installation can be done later for full functionality!
