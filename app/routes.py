#api endpoints
from fastapi import APIRouter
import random
from app.word_list import WORD_DICT

router = APIRouter()

@router.get("/get_word")
def get_word(category: str = None):
    """
    Returns a random word.
    Optional: filter by category if provided.
    """
    if category:
        words = WORD_DICT.get(category, [])
        if not words:
            return {"error": "Invalid category"}
        word = random.choice(words)
    else:
        # Select from all categories
        all_words = [w for cat_words in WORD_DICT.values() for w in cat_words]
        word = random.choice(all_words)

    return {"word": word}
