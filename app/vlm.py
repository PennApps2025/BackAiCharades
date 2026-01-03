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

# 모델 우선순위 (무료 플랜 비전 모델)
# 
# 시스템 설정: 10초 캡처 간격 = 6 calls/min
# 게임당 예상: 4-5회 API 호출 (45초 게임)
# 
# 사용 가능한 비전 모델:
# • gemini-2.5-flash-lite: 10 RPM, 20 RPD - 빠름 (300-800ms)
# • gemini-2.5-flash: 5 RPM, 20 RPD
# 
# 전략: 모델 우선 순회
# 1. 모든 키에서 flash-lite 시도 (Key#1, #2, #3)
# 2. 모든 flash-lite 소진 시 flash 시도 (Key#1, #2, #3)
# 
# 3개 API 키 × 2개 모델 × 20 RPD = 120 calls/day (하루 24게임)
MODEL_PRIORITY = [
    "gemini-2.5-flash-lite",  # 모든 키에서 먼저 시도
#     "gemini-2.5-flash",       # flash-lite 소진 후 사용
#     "gemini-robotics-er-1.5-preview"
]

# 마지막 성공한 조합 기억 (스마트 로테이션)
# 초기값: None으로 시작하여 첫 성공 시 학습
last_successful_key_index = None
last_successful_model = None
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
    Calls the Gemini API with smart rotation (remembers last successful combination).
    Tries last successful combo first, then falls back to sequential search.
    """
    global last_successful_key_index, last_successful_model
    
    # Generate prompt
    prompt = generate_prompt(word, all_choices)
    
    # 마지막 성공 조합이 있으면 먼저 시도 (스마트 로테이션)
    if last_successful_key_index is not None and last_successful_model is not None:
        try:
            key_index = last_successful_key_index
            model_name = last_successful_model
            api_key = API_KEYS[key_index - 1]
            
            print(f"🎯 Smart retry: Key#{key_index} + {model_name}")
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            image = Image.open(io.BytesIO(image_bytes))
            response = model.generate_content([prompt, image])
            
            # 성공한 조합 기억
            last_successful_key_index = key_index
            last_successful_model = model_name
            
            print(f"✅ Success: Key#{key_index} + {model_name}")
            print(f"Original response: {response.text}")
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Last combo failed: {error_msg[:100]}")
            print("⚠️ Switching to next available combo...")
    
    # 모든 API 키와 모델 조합 시도 (모델 우선 순회)
    for model_name in MODEL_PRIORITY:
        for key_index, api_key in enumerate(API_KEYS, 1):
            try:
                print(f"Trying: Key#{key_index} + {model_name}")
                
                # Configure API with current key
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                
                # Prepare image
                image = Image.open(io.BytesIO(image_bytes))
                
                # Make API call
                response = model.generate_content([prompt, image])
                
                # 성공한 조합 기억
                last_successful_key_index = key_index
                last_successful_model = model_name
                
                print(f"✅ Success: Key#{key_index} + {model_name}")
                print(f"Original response: {response.text}")
                return response.text
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Key#{key_index} + {model_name}: {error_msg[:100]}")
                
                # Check if it's a quota error
                if "quota" in error_msg.lower() or "429" in error_msg:
                    print("⚠️ Quota exceeded, trying next...")
                    continue
                else:
                    print("⚠️ Other error, trying next...")
                    continue
    
    # All attempts failed
    print("❌ All API keys and models exhausted")
    return "quota_exceeded"