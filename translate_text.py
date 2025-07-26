import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from typing import Dict, List
import os

class TextTranslator:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.fallback_to_cpu = False
        self.model = None
        self.tokenizer = None
        self.model_name = "facebook/m2m100_418M"
        self.language_codes = {
            'English': 'en',
            'Spanish': 'es', 
            'French': 'fr',
            'German': 'de',
            'Italian': 'it',
            'Portuguese': 'pt',
            'Dutch': 'nl',
            'Russian': 'ru',
            'Chinese': 'zh',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Arabic': 'ar',
            'Hindi': 'hi',
            'Bengali': 'bn',
            'Tamil': 'ta',
            'Telugu': 'te',
            'Marathi': 'mr',
            'Gujarati': 'gu',
            'Urdu': 'ur',
            'Turkish': 'tr',
            'Polish': 'pl',
            'Czech': 'cs',
            'Hungarian': 'hu',
            'Romanian': 'ro',
            'Bulgarian': 'bg',
            'Croatian': 'hr',
            'Serbian': 'sr',
            'Slovak': 'sk',
            'Slovenian': 'sl',
            'Estonian': 'et',
            'Latvian': 'lv',
            'Lithuanian': 'lt',
            'Finnish': 'fi',
            'Swedish': 'sv',
            'Norwegian': 'no',
            'Danish': 'da',
            'Icelandic': 'is'
        }
        
    def load_model(self) -> bool:
        """Load the M2M100 translation model"""
        try:
            print(f"Loading translation model: {self.model_name}")
            print(f"Using device: {self.device}")
            
            # Load tokenizer
            self.tokenizer = M2M100Tokenizer.from_pretrained(
                self.model_name,
                cache_dir="models/translation"
            )
            
            # Load model with fallback handling
            try:
                self.model = M2M100ForConditionalGeneration.from_pretrained(
                    self.model_name,
                    cache_dir="models/translation",
                    torch_dtype=torch.float16 if self.device.type == "cuda" and not self.fallback_to_cpu else torch.float32
                )
                
                if not self.fallback_to_cpu:
                    self.model = self.model.to(self.device)
                    # Test GPU compatibility with a small operation
                    test_input = torch.tensor([[1, 2, 3]]).to(self.device)
                    with torch.no_grad():
                        _ = self.model.get_encoder()(test_input)
                    print("GPU compatibility test passed!")
                else:
                    self.model = self.model.to("cpu")
                    self.device = torch.device("cpu")
                    
            except RuntimeError as e:
                if "no kernel image is available" in str(e) or "CUDA error" in str(e):
                    print(f"GPU compatibility issue detected: {e}")
                    print("Falling back to CPU execution...")
                    self.fallback_to_cpu = True
                    self.device = torch.device("cpu")
                    
                    # Reload model on CPU
                    self.model = M2M100ForConditionalGeneration.from_pretrained(
                        self.model_name,
                        cache_dir="models/translation",
                        torch_dtype=torch.float32
                    ).to("cpu")
                else:
                    raise e
            
            print(f"Translation model loaded successfully on {self.device}!")
            return True
            
        except Exception as e:
            print(f"Error loading translation model: {str(e)}")
            return False
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return list(self.language_codes.keys())
    
    def translate_text(self, text: str, target_language: str, source_language: str = "English") -> str:
        """Translate text from source language to target language"""
        try:
            if self.model is None or self.tokenizer is None:
                if not self.load_model():
                    return None
            
            # Get language codes
            src_lang = self.language_codes.get(source_language, 'en')
            tgt_lang = self.language_codes.get(target_language, 'en')
            
            if src_lang == tgt_lang:
                return text  # No translation needed
            
            # Set source language
            self.tokenizer.src_lang = src_lang
            
            # Tokenize input text
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate translation with error handling
            try:
                with torch.no_grad():
                    generated_tokens = self.model.generate(
                        **inputs,
                        forced_bos_token_id=self.tokenizer.get_lang_id(tgt_lang),
                        max_length=512,
                        num_beams=5,
                        early_stopping=True,
                        do_sample=False
                    )
            except RuntimeError as e:
                if "no kernel image is available" in str(e) or "CUDA error" in str(e):
                    print(f"GPU execution failed: {e}")
                    print("Retrying on CPU...")
                    
                    # Move everything to CPU
                    self.model = self.model.to("cpu")
                    self.device = torch.device("cpu")
                    self.fallback_to_cpu = True
                    
                    # Retry on CPU
                    inputs = {k: v.to("cpu") for k, v in inputs.items()}
                    with torch.no_grad():
                        generated_tokens = self.model.generate(
                            **inputs,
                            forced_bos_token_id=self.tokenizer.get_lang_id(tgt_lang),
                            max_length=512,
                            num_beams=5,
                            early_stopping=True,
                            do_sample=False
                        )
                else:
                    raise e
            
            # Decode translated text
            translated_text = self.tokenizer.batch_decode(
                generated_tokens, 
                skip_special_tokens=True
            )[0]
            
            print(f"Translated '{text}' from {source_language} to {target_language}: '{translated_text}'")
            return translated_text
            
        except Exception as e:
            print(f"Error translating text: {str(e)}")
            return None
    
    def batch_translate(self, texts: List[str], target_language: str, source_language: str = "English") -> List[str]:
        """Translate multiple texts"""
        try:
            if self.model is None or self.tokenizer is None:
                if not self.load_model():
                    return []
            
            translations = []
            for text in texts:
                translated = self.translate_text(text, target_language, source_language)
                translations.append(translated if translated else text)
            
            return translations
            
        except Exception as e:
            print(f"Error in batch translation: {str(e)}")
            return texts  # Return original texts if translation fails
    
    def detect_language(self, text: str) -> str:
        """Simple language detection (placeholder implementation)"""
        # This is a simplified implementation
        # In a real scenario, you might want to use a dedicated language detection library
        
        # Check for common patterns
        if any(char in text for char in ['的', '是', '在', '有', '我', '你', '他']):
            return 'Chinese'
        elif any(char in text for char in ['は', 'を', 'が', 'に', 'と', 'で']):
            return 'Japanese'
        elif any(char in text for char in ['을', '를', '이', '가', '에', '의']):
            return 'Korean'
        elif any(char in text for char in ['है', 'हैं', 'का', 'की', 'के', 'में']):
            return 'Hindi'
        elif any(char in text for char in ['ال', 'في', 'من', 'إلى', 'على', 'هذا']):
            return 'Arabic'
        elif any(char in text for char in ['и', 'в', 'на', 'с', 'по', 'от']):
            return 'Russian'
        else:
            return 'English'  # Default assumption
    
    def get_language_info(self) -> Dict[str, str]:
        """Get information about supported languages"""
        return {
            'model': self.model_name,
            'supported_languages': len(self.language_codes),
            'device': str(self.device),
            'languages': self.language_codes
        }

if __name__ == "__main__":
    # Test the translator
    translator = TextTranslator()
    
    # Test translation
    test_text = "Hello, how are you today?"
    target_lang = "Spanish"
    
    translated = translator.translate_text(test_text, target_lang)
    if translated:
        print(f"Original: {test_text}")
        print(f"Translated to {target_lang}: {translated}")
    
    # Show supported languages
    print(f"\nSupported languages: {translator.get_supported_languages()}")
