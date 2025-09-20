# app/word_list.py

# app/word_list.py

WORD_DICT = {
    # Everyday actions — easy to act out without props, large and clear movements
    "Everyday actions": [
        "waving",        # waving hand left/right
        "clapping",      # clapping hands
        "pointing",      # pointing with finger
        "shrugging",     # shrugging shoulders
        "shaking head",  # shaking head side to side
        "sitting down",  # motion of sitting
        "standing up",   # motion of standing
        "lying down",    # motion of lying down
        "stretching",    # stretching arms/body
        "yawning",       # yawning (open mouth, cover with hand)
        "thumbs up",
        "thumbs down",
        "peace sign",
        "salute",
        "facepalm",
        "hands on hips",
        "covering mouth"
    ],

    # Physical activities — obvious body movement, no props required
    "Physical activities": [
        "jumping",        # jumping motion
        "running",        # running in place
        "skipping",       # skipping motion
        "kicking",        # kicking motion
        "balancing",      # standing on one leg
        "push-up",        # push-up motion
        "sit-up"          # sit-up motion
    ],

    # Emotions — mainly facial expressions, easy for VLM to classify
    "Emotions": [
        "happy",
        "sad",
        "angry",
        "surprised",
        "scared",
        "excited",
        "bored",
        "confused",
        "proud",
        "nervous"
    ],

    # Occupations — chosen so they can be acted out with gestures only
    "Occupations": [
        "dancer",    # dancing motion
        "singer",    # singing or holding mic gesture
        "teacher",   # pointing/explaining gesture
        "chef",      # stirring/cooking motion
        "doctor",    # checking pulse or listening motion
        "artist",    # painting gesture
        "musician"   # playing instrument gesture
    ]
}
