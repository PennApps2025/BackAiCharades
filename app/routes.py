# routes.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.word_list import WORD_DICT
from app.vlm import vlm_guess
import random
from PIL import Image
import io
from app.models import Score
from app.database import submit_score, get_leaderboard as db_get_leaderboard

router = APIRouter()

@router.get("/get_word")
def get_word(category: str = None):
    """
    Returns a random word and a list of choices for the AI.
    """
    if category:
        words = WORD_DICT.get(category, [])
        if not words:
            raise HTTPException(status_code=400, detail="Invalid category")
        word = random.choice(words)
        choices = words # Use all words in the category as choices
    else:
        # Select from all categories if none is specified
        all_words = [w for cat_words in WORD_DICT.values() for w in cat_words]
        word = random.choice(all_words)
        # For a general word, we can pick its category for choices
        for cat, cat_words in WORD_DICT.items():
            if word in cat_words:
                choices = cat_words
                break

    return {"word": word, "choices": choices}


@router.post("/guess")
async def guess(file: UploadFile = File(...), word: str = Form(...), choices: str = Form(...)):
    # --- Pillow Image Preprocessing ---
    try:
        # 1. Read image into bytes
        image_bytes = await file.read()

        # 2. Open image from bytes
        image = Image.open(io.BytesIO(image_bytes))

        # 3. Resize the image (e.g., to max 512x512)
        image.thumbnail((512, 512))

        # 4. Save the processed image back to bytes in JPEG format
        processed_image_io = io.BytesIO()
        image.save(processed_image_io, format='JPEG')
        processed_image_bytes = processed_image_io.getvalue()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid or corrupt image file: {e}")
    # -----------------------------------
    
    # The choices from the frontend will be a comma-separated string, convert to list
    choices_list = [c.strip() for c in choices.split(',')]

    # Call VLM API with the *processed* image bytes and original mime type
    vlm_response = vlm_guess(
        image_bytes=processed_image_bytes, 
        mime_type="image/jpeg", # We converted it to JPEG
        word=word,
        all_choices=choices_list
    )

    clean_response = vlm_response.strip().lower()

    matched_word = None
    for choice in choices_list:
        if choice in clean_response:
            matched_word = choice
            break

    if matched_word:
        result = "success" if matched_word == word.lower() else "fail"
        final_guess = matched_word
    else:
        result = "undetected"
        final_guess = "None"

    return {"guess": final_guess, "result": result, "response": vlm_response}

@router.post("/leaderboard")
def post_score(score: Score):
    submit_score(score)
    return {"message": "Score submitted"}

@router.get("/leaderboard")
def get_leaderboard():
    # Call the database helper to fetch the leaderboard
    data = db_get_leaderboard()
    return data