# vlm.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

# --- Setup ---
load_dotenv()

# API 키 동적 로드 (GEMINI_API_KEY, GEMINI_API_KEY_2, GEMINI_API_KEY_3, ...)
API_KEYS = []
key_index = 1
while True:
    if key_index == 1:
        key = os.getenv("GEMINI_API_KEY")
    else:
        key = os.getenv(f"GEMINI_API_KEY_{key_index}")
    
    if key:
        API_KEYS.append(key)
        print(f"✅ Loaded API Key #{key_index}")
        key_index += 1
    else:
        break  # No more keys found

if not API_KEYS:
    raise ValueError("No GEMINI_API_KEY found in .env file. Add at least GEMINI_API_KEY=your_key")

print(f"📊 Total API Keys loaded: {len(API_KEYS)}")

# 모델 우선순위 (각 모델은 독립적인 20 RPD 할당량)
MODEL_PRIORITY = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3-flash"
]
# -------------

def generate_prompt(word_to_guess: str, choices: list) -> str:
    """Creates a high-quality prompt for the VLM to improve accuracy."""
    # Shuffle the choices to ensure the correct word isn't always in the same spot
    import random
    random.shuffle(choices)
    
    return f"""
You are an AI playing charades. Based on the image provided, pick the word from the list that best matches
the action the person is acting out. Only pick a word if you are more than 40% confident. 
If you pick a word, also explain in 1 short sentence why you chose it. 
If none of the words seem like a reasonable match, respond with a short "not sure" style message. 
Make it playful and casual. 
Do not use Markdown formatting. Your response should be plain text only.  

Choices: {', '.join(choices)}
"""

def vlm_guess(image_bytes: bytes, mime_type: str, word: str, all_choices: list) -> str:
    """
    Calls the Gemini API with multi-model fallback and API key rotation.
    Tries all combinations: Key1+Model1, Key1+Model2, Key1+Model3, Key2+Model1, ...
    """
    # Generate prompt
    prompt = generate_prompt(word, all_choices)
    
    # 모든 API 키와 모델 조합 시도
    for key_index, api_key in enumerate(API_KEYS, 1):
        for model_name in MODEL_PRIORITY:
            try:
                print(f"Trying: Key#{key_index} + {model_name}")
                
                # Configure API with current key
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                
                # Prepare image
                image = Image.open(io.BytesIO(image_bytes))
                
                # Make API call
                response = model.generate_content([prompt, image])
                
                print(f"✅ Success: Key#{key_index} + {model_name}")
                print(f"Original response: {response.text}")
                return response.text
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Key#{key_index} + {model_name}: {error_msg[:100]}")
                
                # Check if it's a quota error
                if "quota" in error_msg.lower() or "429" in error_msg:
                    print("⚠️ Quota exceeded, trying next...")
                    continue  # Try next model/key combination
                else:
                    # Other errors - continue to next combination
                    print(f"⚠️ Other error, trying next...")
                    continue
    
    # All attempts failed
    print("❌ All API keys and models exhausted")
    return "quota_exceeded"