# app/word_list.py

# app/word_list.py

WORD_DICT = {
    # Everyday actions — easy to act out without props, large and clear movements
    "Everyday actions": [
        "waving",        # waving hand left/right
        "clapping",      # clapping hands
        "pointing",      # pointing with finger
        "shrugging",     # shrugging shoulders
        "sitting down",  # motion of sitting
        "standing up",   # motion of standing
        "stretching",    # stretching arms/body
        "yawning",       # yawning (open mouth, cover with hand)
        "kicking",        # kicking motion
        "punching",
        "thumbs up",
        "thumbs down",
        "peace sign",
        "salute",
        "hands on hips",
        "covering mouth",
        "swimming"
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
        "nervous"
    ],

    # Occupations — chosen so they can be acted out with gestures only
    "Occupations": [
        "ballet dancer",    # dancing motion
        "singer",    # singing or holding mic gesture
        "teacher",   # pointing/explaining gesture
        "doctor",    # checking pulse or listening motion
        "pianist",  # playing piano
        "guitarist", # playing guitar
        "photographer",
        "solider",
        "waiter / waitress",
        "boxer",
        "swimmer",
        "rock climber"
    ],

    "Animals": [
        "bird",
        "fish",
        "rabbit",
        "horse",
        "frog",
        "elephant",
        "monkey",
        "bear",
        "giraffe",
        "kangaroo",
        "snake"
    ]
}
