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


# Image upload limits
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGE_PIXELS = 10_000_000  # 10 million pixels (e.g., 4000x2500)

@router.post("/guess")
async def guess(file: UploadFile = File(...), word: str = Form(...), choices: str = Form(...)):
    # --- Image Size Validation ---
    # 1. Check file size limit to prevent memory exhaustion
    chunks = []
    total_size = 0
    chunk_size = 1024 * 1024  # Read 1MB at a time
    
    try:
        while chunk := await file.read(chunk_size):
            total_size += len(chunk)
            if total_size > MAX_IMAGE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"Image too large. Maximum size is {MAX_IMAGE_SIZE / (1024*1024):.0f}MB."
                )
            chunks.append(chunk)
        
        image_bytes = b''.join(chunks)
        
        if total_size == 0:
            raise HTTPException(status_code=400, detail="Empty file received")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {e}")
    
    # --- Pillow Image Preprocessing ---
    try:
        # 2. Verify it's a valid image
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()  # Verify image integrity
        
        # Re-open after verify (verify() makes image unusable)
        image = Image.open(io.BytesIO(image_bytes))
        
        # 3. Check pixel dimensions to prevent decompression bombs
        if image.width * image.height > MAX_IMAGE_PIXELS:
            raise HTTPException(
                status_code=413,
                detail=f"Image resolution too high. Maximum is {MAX_IMAGE_PIXELS:,} pixels."
            )
        
        # 4. Resize the image (e.g., to max 512x512)
        image.thumbnail((512, 512))

        # 5. Save the processed image back to bytes in JPEG format
        processed_image_io = io.BytesIO()
        image.save(processed_image_io, format='JPEG')
        processed_image_bytes = processed_image_io.getvalue()

    except HTTPException:
        raise
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


    # Check if quota exceeded
    if vlm_response == "quota_exceeded":
        raise HTTPException(
            status_code=429,
            detail="Thanks for playing! 🎮 This demo has a daily limit to keep it free for everyone. We've reached today's limit, but you can try again tomorrow! See you then! ⏰"
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