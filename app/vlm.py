# vlm.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Setup ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-lite')
# -------------

def generate_prompt(word_to_guess: str, choices: list) -> str:
    """Creates a high-quality prompt for the VLM to improve accuracy."""
    # Shuffle the choices to ensure the correct word isn't always in the same spot
    import random
    random.shuffle(choices)
    
    return f"""
You are an AI playing charades. Based on the image provided, pick the word from the list that best matches
the action the person is acting out. Only pick a word if you are at least 50% confident. 
If you pick a word, also explain in 1 short sentence why you chose it. 
If none of the words seem like a reasonable match, respond with a short "not sure" style message. 
Make it playful and casual. 
Do not use Markdown formatting. Your response should be plain text only.  

Choices: {', '.join(choices)}
"""

def vlm_guess(image_bytes: bytes, mime_type: str, word: str, all_choices: list) -> str:
    """
    Calls the Gemini Pro Vision API with preprocessed image bytes and returns the AI's guess.
    """
    image_part = {
        "mime_type": mime_type,
        "data": image_bytes
    }

    # Generate a better prompt with multiple choices
    prompt = generate_prompt(word, all_choices)

    try:
        # Make the API call
        response = model.generate_content([prompt, image_part])
        return response.text
    except Exception as e:
        print(f"Gemini API call error: {e}")
        return "error"