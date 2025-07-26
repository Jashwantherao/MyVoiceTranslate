#!/usr/bin/env python3
"""
Performance test for MyVoiceTranslate application
Tests translation functionality with GPU fallback handling
"""

import time
import torch
from translate_text import TextTranslator

def test_translation_performance():
    """Test translation performance and GPU fallback"""
    print("=== MyVoiceTranslate Performance Test ===\n")
    
    # System info
    print("🖥️ System Information:")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU device: {torch.cuda.get_device_name(0)}")
        print(f"CUDA version: {torch.version.cuda}")
    print()
    
    # Initialize translator
    print("🔄 Initializing translator...")
    translator = TextTranslator()
    print(f"Initial device: {translator.device}")
    print()
    
    # Test sentences in different languages
    test_cases = [
        ("Hello, how are you today?", "English", "Spanish"),
        ("Good morning, I hope you have a great day!", "English", "French"),
        ("Technology is advancing rapidly.", "English", "German"),
        ("The weather is beautiful today.", "English", "Italian"),
        ("Thank you for your help.", "English", "Portuguese")
    ]
    
    print("🌍 Testing translations...")
    total_start_time = time.time()
    
    for i, (text, source_lang, target_lang) in enumerate(test_cases, 1):
        print(f"\n--- Test {i}/5 ---")
        print(f"Input: {text}")
        print(f"Translating from {source_lang} to {target_lang}...")
        
        start_time = time.time()
        result = translator.translate_text(text, target_lang, source_lang)
        end_time = time.time()
        
        if result:
            print(f"✅ Result: {result}")
            print(f"⏱️ Time: {end_time - start_time:.2f} seconds")
        else:
            print("❌ Translation failed")
        
        print(f"Device used: {translator.device}")
        if hasattr(translator, 'fallback_to_cpu') and translator.fallback_to_cpu:
            print("⚠️ Using CPU fallback")
    
    total_time = time.time() - total_start_time
    print(f"\n🏁 Total test time: {total_time:.2f} seconds")
    print(f"Average per translation: {total_time/len(test_cases):.2f} seconds")
    
    # Final status
    print("\n📊 Final Status:")
    print(f"Device: {translator.device}")
    if hasattr(translator, 'fallback_to_cpu'):
        if translator.fallback_to_cpu:
            print("Status: ⚠️ CPU fallback mode (GPU incompatible)")
        else:
            print("Status: ✅ GPU acceleration active")
    
    print("\n✅ Performance test completed!")

if __name__ == "__main__":
    test_translation_performance()
