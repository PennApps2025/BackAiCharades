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
model = genai.GenerativeModel('gemini-1.5-flash')
# -------------

def generate_prompt(word_to_guess: str, choices: list) -> str:
    """Creates a high-quality prompt for the VLM to improve accuracy."""
    # Shuffle the choices to ensure the correct word isn't always in the same spot
    import random
    random.shuffle(choices)
    
    return f"""
You are an expert at the game of charades.
Based on the following image, which of these words is the person trying to act out?
Your answer must be exactly one word from the list provided.

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
        # Clean up the response text
        result_text = response.text.strip().lower()
        return result_text
    except Exception as e:
        print(f"Gemini API call error: {e}")
        return "error"