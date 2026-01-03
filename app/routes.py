# routes.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.word_list import WORD_DICT
from app.vlm import vlm_guess
import random
from PIL import Image
import io
from app.models import Score
from app.database import submit_score, get_leaderboard as db_get_leaderboard
import uuid
from datetime import datetime, timedelta

router = APIRouter()

# Session management
active_session = {
    "session_id": None,
    "started_at": None,
    "expires_at": None
}
SESSION_TIMEOUT = 120  # 2 minutes timeout

# Session management
active_session = {
    "session_id": None,
    "started_at": None,
    "expires_at": None
}
SESSION_TIMEOUT = 60  # 60 seconds timeout

@router.post("/start_session")
def start_session():
    """
    Acquire a game session. Only one player can play at a time.
    """
    global active_session
    now = datetime.now()
    
    # Check if there's an active session that hasn't expired
    if active_session["session_id"] and active_session["expires_at"]:
        if now < active_session["expires_at"]:
            raise HTTPException(
                status_code=409, 
                detail="Game in progress. Please wait."
            )
    
    # Create new session
    session_id = str(uuid.uuid4())
    active_session["session_id"] = session_id
    active_session["started_at"] = now
    active_session["expires_at"] = now + timedelta(seconds=SESSION_TIMEOUT)
    
    print(f"🎮 Session started: {session_id[:8]}")
    return {"session_id": session_id, "expires_at": active_session["expires_at"].isoformat()}

@router.post("/heartbeat")
def heartbeat(session_id: str = Form(...)):
    """
    Keep the session alive by updating expiration time.
    """
    global active_session
    now = datetime.now()
    
    if active_session["session_id"] == session_id:
        # Extend session
        active_session["expires_at"] = now + timedelta(seconds=SESSION_TIMEOUT)
        return {"message": "Session extended", "expires_at": active_session["expires_at"].isoformat()}
    
    raise HTTPException(status_code=404, detail="Session not found")

@router.post("/end_session")
def end_session(session_id: str = Form(...)):
    """
    Release the game session.
    """
    global active_session
    
    if active_session["session_id"] == session_id:
        print(f"✅ Session ended: {session_id[:8]}")
        active_session["session_id"] = None
        active_session["started_at"] = None
        active_session["expires_at"] = None
        return {"message": "Session ended"}
    
    return {"message": "Session not found or already ended"}

@router.get("/check_session")
def check_session():
    """
    Check if a game session is currently active.
    """
    global active_session
    now = datetime.now()
    
    if active_session["session_id"] and active_session["expires_at"]:
        if now < active_session["expires_at"]:
            return {
                "active": True,
                "expires_at": active_session["expires_at"].isoformat()
            }
    
    return {"active": False}

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