# Configuration file for MyVoiceTranslate

# Model Configuration
MODEL_CONFIG = {
    'translation_model': 'facebook/m2m100_418M',
    'voice_cloning_model': 'openvoice',
    'sample_rate': 24000,
    'max_audio_duration': 30.0,
    'min_audio_duration': 1.0,
    'batch_size': 1,
    'max_sequence_length': 512
}

# GPU Configuration
GPU_CONFIG = {
    'use_gpu': True,
    'gpu_memory_fraction': 0.9,
    'mixed_precision': True,
    'device_map': 'auto'
}

# Audio Configuration
AUDIO_CONFIG = {
    'sample_rate': 24000,
    'bit_depth': 16,
    'channels': 1,
    'format': 'wav',
    'normalization_db': -20.0,
    'silence_threshold_db': 20
}

# UI Configuration
UI_CONFIG = {
    'max_file_size_mb': 100,
    'supported_formats': ['wav', 'mp3', 'm4a', 'flac'],
    'max_text_length': 1000,
    'default_source_language': 'English',
    'default_target_language': 'Spanish'
}

# Paths Configuration
PATHS = {
    'models_dir': 'models',
    'samples_dir': 'samples',
    'outputs_dir': 'outputs',
    'processed_dir': 'samples/processed',
    'checkpoints_dir': 'models/checkpoints',
    'translation_cache': 'models/translation'
}

# Language Configuration
SUPPORTED_LANGUAGES = {
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

# Development Configuration
DEV_CONFIG = {
    'debug_mode': False,
    'log_level': 'INFO',
    'enable_profiling': False,
    'mock_voice_cloning': True,  # Set to False when OpenVoice is properly integrated
    'save_intermediate_files': False
}
